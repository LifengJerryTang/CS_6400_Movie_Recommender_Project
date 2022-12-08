import torch
from torch import nn
from collections import OrderedDict
from module_utils import ReduceMapping, TextEncoder
from dataset import RatingDataset

class EmbeddingCluster(torch.nn.Module):
    '''
    configs = {FeatureName: [NumEmbed, EmbedLen, PaddingIdx], ...}
    '''
    def __init__(self, configs={'feature1': [100, 32, 0], 'feature2': [100, 32, 0]}, **factory_kwargs):
        super(EmbeddingCluster, self).__init__()
        self.configs = configs
        self.embeddings = torch.nn.ModuleDict({k:torch.nn.Embedding(v[0], v[1], padding_idx=v[2], 
                                                                    **factory_kwargs) for k,v in configs.items()})
    def rotate_embedding(self, x, names: list):
        '''
        torch.LongTensor([[Feature1, Feature2], [Feature1, Feature2], [Feature1, Feature2]])
        torch.LongTensor([[1, 2], [2, 0], [3, 2]]) -> torch.Tensor([[vector0...], [vector1...], [vector2...]])
        '''
        embs = [self.embeddings[n] for n in names]
        return torch.cat([embs[i](x[:, i]) for i in range(x.shape[-1])], dim=1)
    def multiple_rotate_embedding(self, x, names: list):
        '''
        torch.LongTensor([
                        [[Feature1, Feature2, Feature3], [Feature1, Feature2, Feature3], ...],
                        [[Feature1, Feature2, Feature3], [Feature1, Feature2, Feature3], ...],
                        ...
                        ])
        torch.LongTensor([[[1,2,3], [1,2,4], [0,2,5], [0,2,5]],
                        [[3,1,3], [2,4,2], [1,1,5], [1,1,5]]])
        =====>
        torch.Tensor([[VectorF123, VectorF123, ...], 
                    [VectorF123, VectorF123, ...]])
        size([2,4,3]) -> size([8,3]) -> size([8, vlen_sum] -> size([2,4,vlen_sum]))
        '''
        return self.rotate_embedding(x=x.reshape(x.shape[-3]*x.shape[-2], -1), names=names).reshape(x.shape[-3], x.shape[-2], -1)
    def match_names(self, name_initial:str):
        return [i for i in self.embeddings.keys() if i[0:len(name_initial)]==name_initial]
    def match_name_embedding(self, x, name_initial, embed_type='rotate_embedding'):
        if embed_type == 'rotate_embedding':
            return self.rotate_embedding(x, self.match_names(name_initial))
        elif embed_type == 'multiple_rotate_embedding':
            return self.multiple_rotate_embedding(x, self.match_names(name_initial))
    def get_embedding_length(self, name_initial):
        return sum([self.configs[i][1] for i in self.match_names(name_initial)])
    def get_embedding_by_name(self, name_initial):
        return [self.embeddings[i] for i in self.match_names(name_initial)]
    def forward(self):
        pass

class MLPMapping(torch.nn.Module):
    def __init__(self, input_len=128, output_len=128, mlp_ratio=4, dropout=0., **factory_kwargs):
        super(MLPMapping, self).__init__()
        self.mapping = torch.nn.Sequential(
                    torch.nn.Linear(input_len, (mlp_ratio//2)*input_len, **factory_kwargs),
                    torch.nn.Dropout(dropout),
                    torch.nn.GELU(),
                    torch.nn.Linear((mlp_ratio//2)*input_len, mlp_ratio*input_len, **factory_kwargs),
                    torch.nn.Dropout(dropout),
                    torch.nn.GELU(),
                    torch.nn.Linear(mlp_ratio*input_len, output_len, **factory_kwargs), 
                )
        self.shortcut = torch.nn.Linear(input_len, output_len, **factory_kwargs)
    def forward(self, x):
        return self.mapping(x) + self.shortcut(x)

class FusionModel(torch.nn.Module):
    def __init__(self, ds:RatingDataset, embedding_configs:dict, output_len = 128, 
                       avgpooling_output_len = 128, text_encoder_output_len = 128, **factory_kwargs):
        super().__init__()
        self.ds, self.embedding_configs = ds, embedding_configs
        self.embc = EmbeddingCluster(configs=embedding_configs)
        self.avgpooling_configs = {n:[ReduceMapping, dict(encoded_dim=self.embc.get_embedding_length(n),
                                                    cond_dim=512, output_dim=avgpooling_output_len,
                                                    attn_depth=2, attn_dim_head=64, attn_heads=8,
                                                    attn_num_latents=32, attn_cosine_sim_attn=False,
                                                    perceiver=False)
                                ] for n in ds.avgpooling_variables}
        self.avgpooling = torch.nn.ModuleDict({n: self.avgpooling_configs[n][0](**self.avgpooling_configs[n][1]) for n in self.avgpooling_configs})       
        self.text_encoder = TextEncoder(cond_dim=512, output_dim=text_encoder_output_len,
                                attn_depth=2, attn_dim_head=64, attn_heads=8,
                                attn_num_latents=32, attn_cosine_sim_attn=False)
        movie_feature_len = len(ds.numerical_variables) + \
                            sum([self.embc.get_embedding_length(n) for n in ds.categorical_variables]) + \
                            len(ds.avgpooling_variables)*avgpooling_output_len + \
                            text_encoder_output_len
        user_feature_len = self.embc.get_embedding_length('userId') + 1

        self.movie_mapping = MLPMapping(input_len=movie_feature_len, output_len=output_len, mlp_ratio=4, dropout=0.)
        self.user_mapping = MLPMapping(input_len=user_feature_len, output_len=output_len, mlp_ratio=4, dropout=0.)
        self.on_cpu = False

    def forward(self, d, external_loss_calculation=False):
        # d[0]: Input Variables, d[1]: Ground Truth Rating Score
        movie_features = OrderedDict()
        for n in self.ds.numerical_variables:
            movie_features[n] = d[0][self.ds.order_dict[n]].to(torch.float32).reshape(-1, 1)
        for n in self.ds.categorical_variables:
            x = d[0][self.ds.order_dict[n]]
            movie_features[n] = self.embc.match_name_embedding(x,  name_initial=n, embed_type='rotate_embedding')
        for n in self.ds.avgpooling_variables:
            #print(f'Current n: {n}', end=' ... ')
            x = d[0][self.ds.order_dict[n]]
            cemb = self.embc.match_name_embedding(x,  name_initial=n, embed_type='multiple_rotate_embedding')
            movie_features[n] = self.avgpooling[n](cemb)
            #print(f'Finished')
        movie_features['prompt'] = self.text_encoder(d[0][self.ds.order_dict['prompt']], cpu=self.on_cpu)
        movie_features = torch.cat(list(movie_features.values()), dim=1)

        user_features = OrderedDict()
        user_features['userId'] = self.embc.match_name_embedding(d[0][self.ds.order_dict['userId']],  name_initial='userId', embed_type='rotate_embedding')
        user_features['timestamp'] = d[0][self.ds.order_dict['timestamp']].reshape(-1, 1).to(torch.float32)
        user_features = torch.cat(list(user_features.values()), dim=1)
        
        movie_features = self.movie_mapping(movie_features)
        user_features = self.user_mapping(user_features)
        
        if not external_loss_calculation:
            cross = torch.nn.functional.cosine_similarity(movie_features, user_features, dim=1, eps=1e-08)
            mse = torch.nn.functional.mse_loss(cross, d[1].to(torch.float32))
            return mse
        else:
            return movie_features, user_features

    def calculate_movie_feature(self, d, movie_ds):
        # d: Movie Input Variables
        movie_features = OrderedDict()
        for n in movie_ds.numerical_variables:
            movie_features[n] = d[movie_ds.order_dict[n]].to(torch.float32).reshape(-1, 1)
        for n in movie_ds.categorical_variables:
            x = d[movie_ds.order_dict[n]]
            movie_features[n] = self.embc.match_name_embedding(x,  name_initial=n, embed_type='rotate_embedding')
        for n in movie_ds.avgpooling_variables:
            #print(f'Current n: {n}', end=' ... ')
            x = d[movie_ds.order_dict[n]]
            cemb = self.embc.match_name_embedding(x,  name_initial=n, embed_type='multiple_rotate_embedding')
            movie_features[n] = self.avgpooling[n](cemb)
            #print(f'Finished')
        movie_features['prompt'] = self.text_encoder(d[movie_ds.order_dict['prompt']], cpu=self.on_cpu)
        movie_features = torch.cat(list(movie_features.values()), dim=1)
        movie_features = self.movie_mapping(movie_features)
        return movie_features
    
    def calculate_user_feature(self, d, user_ds, external_timestamp=None):
        # d: User Input Variables
        user_features = OrderedDict()
        user_features['userId'] = self.embc.match_name_embedding(d[0],  name_initial='userId', embed_type='rotate_embedding')
        if external_timestamp is None:
            user_features['timestamp'] = d[1].reshape(-1, 1).to(torch.float32)
        else:
            shape = d[0].shape[0]
            user_features['timestamp'] = torch.Tensor([external_timestamp for i in range(shape)]).to(d[0].device).reshape(-1, 1).to(torch.float32)
        user_features = torch.cat(list(user_features.values()), dim=1)
        user_features = self.user_mapping(user_features)
        return user_features
    
    def cpu(self):
        self.on_cpu = True
        return super().cpu()
        
    def cuda(self):
        self.on_cpu = False
        return super().cuda()