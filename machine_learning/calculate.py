from dataset import RatingDataset, RatingDatasetMovie, RatingDatasetUser
import time
import sqlite3
import pandas as pd
import torch
from model import FusionModel
import json

def get_timestamp(call_time = "2022-12-25 00:00:00"):
    call_timestamp = int(time.mktime(time.strptime(call_time, "%Y-%m-%d %H:%M:%S")))
    transformed_call_timestamp = ds.trackers['timestamp'].transform(call_timestamp)
    return transformed_call_timestamp

if __name__ == '__main__':
    conn_path = 'dataset.db'
    conn = sqlite3.connect(conn_path)
    ds = RatingDataset(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0, 0.8], verbose=False, load_from_path="ds.pkl")
    ds_movie = RatingDatasetMovie(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0, 1], verbose=False, load_from_path="ds.pkl")
    ds_user = RatingDatasetUser(ds.trackers['userId'], fix_timestamp=get_timestamp())
    with open('embedding_configs.json') as f:
        embedding_configs = json.load(f)
    model = FusionModel(ds=ds, embedding_configs=embedding_configs, output_len = 128, avgpooling_output_len = 128, text_encoder_output_len = 128)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        model.load_state_dict(torch.load('model_image.pkl', map_location='cuda'))
        model = model.cuda()
    else:
        model.load_state_dict(torch.load('model_image.pkl', map_location='cpu'))
        model = model.cpu()
    model = model.eval()
    batch_size = 64
    data_movie = torch.utils.data.DataLoader(ds_movie, 
                                            batch_size=batch_size, 
                                            num_workers=0,
                                            shuffle=False,
                                            pin_memory=False
                                            )
    data_user = torch.utils.data.DataLoader(ds_user, 
                                            batch_size=batch_size, 
                                            num_workers=0,
                                            shuffle=False,
                                            pin_memory=False
                                            )
    current = 0
    res = []
    for d in data_movie:
        for ic in range(len(d)):
            try:
                d[ic] = d[ic].to(device)
            except Exception as e:
                #print(e, end=' ')
                pass
        with torch.no_grad():
            movie_feature = model.calculate_movie_feature(d, movie_ds=ds_movie)
        for i in range(movie_feature.shape[0]):
            s = ds_movie.get_original_form(current)
            s['movie_feature'] = movie_feature[i].to(torch.float16).detach().cpu().numpy().tolist()
            res.append(s)
            current += 1
            if current % 2000 == 0:
                print(f'Calculating Movie Representations: Step {current}')
    df = pd.DataFrame(res).reset_index(drop=True)
    df.to_csv('movie_feature_calculated.csv')
    
    current = 0
    res = []
    for d in data_user:
        if current % 10*batch_size-1 == 0:
            print(f'Calculating User Representations: Step {current}')
        for ic in range(len(d)):
            try:
                d[ic] = d[ic].to(device)
            except Exception as e:
                #print(e, end=' ')
                pass
        with torch.no_grad():
            res1 = model.calculate_user_feature(d, user_ds=ds_user, external_timestamp=get_timestamp("2023-01-01 00:00:00"))
            res2 = model.calculate_user_feature(d, user_ds=ds_user, external_timestamp=get_timestamp("2022-01-01 00:00:00"))
            res3 = model.calculate_user_feature(d, user_ds=ds_user, external_timestamp=get_timestamp("2020-01-01 00:00:00"))
            res4 = model.calculate_user_feature(d, user_ds=ds_user, external_timestamp=get_timestamp("2015-01-01 00:00:00"))
            res5 = model.calculate_user_feature(d, user_ds=ds_user, external_timestamp=get_timestamp("2010-01-01 00:00:00"))
        for i in range(res1.shape[0]):
            res_element = {'userId': ds_user.order[current]}
            res_element['user_feature_20230101'] = res1[i].to(torch.float16).detach().cpu().numpy().tolist()
            res_element['user_feature_20220101'] = res2[i].to(torch.float16).detach().cpu().numpy().tolist()
            res_element['user_feature_20200101'] = res3[i].to(torch.float16).detach().cpu().numpy().tolist()
            res_element['user_feature_20150101'] = res4[i].to(torch.float16).detach().cpu().numpy().tolist()
            res_element['user_feature_20100101'] = res5[i].to(torch.float16).detach().cpu().numpy().tolist()
            current += 1
            if current % 2000 == 0:
                print(f'Calculating Movie Representations: Step {current}')
            res.append(res_element)
    df = pd.DataFrame(res).reset_index(drop=True)
    df.to_csv('user_feature_calculated.csv')
