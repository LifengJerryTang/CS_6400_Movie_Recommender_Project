from typing import Iterable
import json
from collections import defaultdict
import pandas as pd
import numpy as np
import torch
import dill as pickle
import sqlite3

class RatingDataset(torch.utils.data.Dataset):
    def __init__(self, fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=None, row_range=[0,1], verbose=False, load_from_path=False):
        self.fetch_type = fetch_type
        self.rating_table = rating_table
        self.movie_table = movie_table
        self.verbose = verbose
        self.conn = None
        self.conn_path = conn_path
        self.row_range = row_range
        self.order = ['revenue', 'budget', 'runtime', 'popularity', 'vote_average', 'vote_count', 'release_date_timestamp', 'timestamp',
                    'adult', 'belongs_to_collection', 'id', 'status', 'have_release_date',
                    'genres', 'spoken_languages', 'production_companies', 'production_countries', 'keywords', 'cast', 'crew',
                    'prompt', 'userId', 'rating']
        self.order_dict = {k:i for k,i in zip(self.order, range(len(self.order)))}
        # names: list[str] -> index: list[int]
        self.order_mapping = lambda names: [self.order_dict[n] for n in names]
        self.init_len()
        super().__init__()
        self.numerical_variables = ['revenue', 'budget', 'runtime', 'popularity', 'vote_average', 'vote_count', 'release_date_timestamp']
        self.categorical_variables = ['adult', 'belongs_to_collection', 'id', 'status', 'have_release_date']
        self.avgpooling_variables = ['genres', 'spoken_languages', 'production_companies', 'production_countries', 'keywords', 'cast', 'crew']
        # sequential_variables = ['cast', 'crew']
        self.prompt_variables = ['genres', 'release_date', 'title', 'production_companies', 'production_countries', 'tagline',
                            'keywords', 'overview']
        self.user_variables = ['userId', 'timestamp', 'rating']

        self.prompt_variables_configs = {
            'prompt': [PromptFeatureTracker, dict(name='prompt', including=self.prompt_variables, verbose=verbose), dict()]
        }
        if not load_from_path:
            self.trackers = {
                                **{k:v[0](**v[1]).track(**v[2]) for k, v in self.numerical_variable_configs.items()}, 
                                **{k:v[0](**v[1]).track(**v[2]) for k, v in self.categorical_variable_configs.items()}, 
                                **{k:v[0](**v[1]).track(**v[2]) for k, v in self.avgpooling_variables_configs.items()}, 
                                **{k:v[0](**v[1]).track(**v[2]) for k, v in self.prompt_variables_configs.items()}
                            }
        else:
            self.load(load_from_path)
    @property
    def numerical_variable_configs(self):
        res = {
            'revenue': [NumericalFeatureTracker, dict(name='revenue', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='revenue')],
            'budget': [NumericalFeatureTracker, dict(name='budget', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='budget')],
            'runtime': [NumericalFeatureTracker, dict(name='runtime', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='runtime')],
            'popularity': [NumericalFeatureTracker, dict(name='popularity', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='popularity')],
            'vote_average': [NumericalFeatureTracker, dict(name='vote_average', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='vote_average')],
            'vote_count': [NumericalFeatureTracker, dict(name='vote_count', transform_type='normalization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='vote_count')],
            'release_date_timestamp': [NumericalFeatureTracker, dict(name='release_date_timestamp', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='release_date_timestamp')],
            
            'timestamp': [NumericalFeatureTracker, dict(name='timestamp', transform_type='standardization', verbose=self.verbose), dict(conn=self.conn_path, table='ratings', column='timestamp')],
            
            'rating': [NumericalFeatureTracker, dict(name='rating', transform_type='rating', verbose=self.verbose), dict(conn=self.conn_path, table='ratings', column='rating')],
        }
        return res
    @property
    def categorical_variable_configs(self):
        return {
            'adult': [CategoricalFeatureTracker, dict(name='adult', transform_type='single_column', tracker_type='db', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='adult')],
            'belongs_to_collection': [CategoricalFeatureTracker, dict(name='belongs_to_collection', tracker_type='db', transform_keys=['name'], verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='belongs_to_collection')],
            'id': [CategoricalFeatureTracker, dict(name='id', transform_type='single_column', tracker_type='db', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='id')],
            'status': [CategoricalFeatureTracker, dict(name='status', transform_type='single_column', tracker_type='db', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='status')],
            'have_release_date': [CategoricalFeatureTracker, dict(name='have_release_date', transform_type='single_column', tracker_type='db', verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='have_release_date')],
            
            'userId': [CategoricalFeatureTracker, dict(name='userId', transform_type='single_column', tracker_type='db', verbose=self.verbose), dict(conn=self.conn_path, table='ratings', column='userId')],
        }
    @property
    def avgpooling_variables_configs(self):
        return {
            'genres': [MultipleCategoricalFeatureTracker, dict(name='genres', tracker_type='db', transform_keys=['name'], min_len=7, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='genres')],
            'spoken_languages': [MultipleCategoricalFeatureTracker, dict(name='spoken_languages', tracker_type='db', transform_keys=['iso_639_1'], min_len=6, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='spoken_languages')],
            'production_companies': [MultipleCategoricalFeatureTracker, dict(name='production_companies', tracker_type='db', transform_keys=['name'], min_len=9, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='production_companies')],
            'production_countries': [MultipleCategoricalFeatureTracker, dict(name='production_countries', tracker_type='db', transform_keys=['iso_3166_1'], min_len=4, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='production_countries')],
            'keywords': [MultipleCategoricalFeatureTracker, dict(name='keywords', tracker_type='db', transform_keys=['name'], min_len=60, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='keywords')],
            'cast': [MultipleCategoricalFeatureTracker, dict(name='cast', tracker_type='db', transform_keys=['name', 'order', 'character', 'gender', 'credit_id'], min_len=128, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='cast')],
            'crew': [MultipleCategoricalFeatureTracker, dict(name='crew', tracker_type='db', transform_keys=['name', 'department', 'gender', 'job', 'credit_id'], min_len=192, verbose=self.verbose), dict(conn=self.conn_path, table='movies', column='crew')],
        }
    def build_conn(self):
        self.conn = sqlite3.connect(self.conn_path)
    def remove_conn(self):
        del self.conn
        self.conn = None
    def __getitem__(self, i):
        s = self.get_original_form(i)
        res = [self.trackers[k].transform(s[self.trackers[k].including]) for k in self.order]
        return res[0:-1], res[-1]
    def get_original_form(self, i, get_row=False):
        row = i+self.start
        fetch_cols = '''r.row_id, r.userId, r.movieId, r.rating, r.timestamp,
                        r.id, m.cast, m.crew, m.keywords, m.adult, 
                        m.belongs_to_collection, m.budget, m.genres, m.homepage, 
                        m.imdb_id, m.original_language, m.original_title, m.overview, 
                        m.popularity, m.poster_path, m.production_companies, m.production_countries, 
                        m.release_date, m.release_date_timestamp, m.have_release_date, m.revenue, 
                        m.runtime, m.spoken_languages, m.status, 
                        m.tagline, m.title, m.vote_average, m.vote_count'''
        sql = f'''
                select {fetch_cols} from
                (select * from `{self.rating_table}`
                where row_id == {row}) as r
                left join `{self.movie_table}` as m
                on r.id = m.id
                '''
        #conn.execute(sql, row).fetchall()
        if self.conn is None:
            self.build_conn()
        s = pd.read_sql(sql, self.conn).iloc[0]
        if get_row:
            return s, row
        return s
    def query_by_id(self, userId=None, movieId=None):
        # userId: List
        id_type = 'userId' if userId is not None else 'movieId'
        cid = userId if userId is not None else movieId
        fetch_cols = '''r.row_id, r.userId, r.movieId, r.rating, r.timestamp,
                        r.id, m.cast, m.crew, m.keywords, m.adult, 
                        m.belongs_to_collection, m.budget, m.genres, m.homepage, 
                        m.imdb_id, m.original_language, m.original_title, m.overview, 
                        m.popularity, m.poster_path, m.production_companies, m.production_countries, 
                        m.release_date, m.release_date_timestamp, m.have_release_date, m.revenue, 
                        m.runtime, m.spoken_languages, m.status, 
                        m.tagline, m.title, m.vote_average, m.vote_count'''
        sql = f'''
                select {fetch_cols} from
                (select * from `{self.rating_table}`
                where {id_type} in {str(cid)}) as r
                left join `{self.movie_table}` as m
                on r.id = m.id
                '''
        if self.conn is None:
            self.build_conn()
        df = pd.read_sql(sql, self.conn)
        return df
    def init_len(self):
        self.build_conn()
        self.full_len = pd.read_sql(f'select max(row_id) from `{self.rating_table}`', self.conn).iloc[0][0]
        self.remove_conn()
        self.start = int(self.row_range[0]*self.full_len)
        self.end = int(self.row_range[1]*self.full_len)
    def __len__(self):
        return self.end - self.start - 2
    def get_embedding_mapping(self, cate_var):
        return {cate_var+'::'+i:len(self.trackers[cate_var].stat[i]) for i in self.trackers[cate_var].stat.keys()}
    def save(self, path):
        print('Saving Dataset To {}'.format(path), end=' ... ')
        with open (path, 'wb') as f:
            pickle.dump(self.trackers, f)
        print('Finished')
    def load(self, path):
        print('Loading Dataset From {}'.format(path), end=' ... ')
        with open (path, 'rb') as f:
            self.trackers = pickle.load(f)
        print('Finished')


class FeatureTracker(object):
    nums = 0
    def __init__(self, name=None, tracker_type='db', including=None, verbose=False, default=0):
        assert tracker_type in ['db', 'iterable']
        if name is not None: self.name = name
        else: self.name = f'feature_{FeatureTracker.nums}'; FeatureTracker.nums += 1
        self.including = including if including is not None else name
        self.default = 0     # default value for categorical features
        #self.including = [self.including] if type(self.including) is str else self.including
        self.tracker_type, self.stat, self.inverse_stat, self.verbose = tracker_type, {}, {}, verbose
    def change_tracker_type(self, tracker_type):
        self.tracker_type = tracker_type
        return self
    @property
    def stat_head(self):
        return f'{self.stat}'[0:200]
    @staticmethod
    def validate_value_by_key(x, key):
        try: eval(str(x))[key]; return True
        except: return False
    @staticmethod
    def extract_value_by_key(x, key):
        return eval(str(x))[key]
    @staticmethod
    def extract_value_list(x):
        try: return eval(x)
        except: return []
    def track(self):
        if self.verbose:
            self.summary()
        return self
    def transform(self):
        # transform a scalar
        NotImplemented
    def inverse_transform(self):
        NotImplemented
    def summary(self):
        print(f'----------------- \n Feature: {self.name} | Type: {self.tracker_type} \n Statistics: \n {self.stat_head} \n -----------------')
        return self

class NumericalFeatureTracker(FeatureTracker):
    def __init__(self, transform_type='normalization', transform_func=None, **kwargs):
        super().__init__(**kwargs)
        self.transform_type = transform_type
        self.transform_func = {'normalization': lambda d: (d - self.stat['min'])/(self.stat['max'] - self.stat['min']),
                               'standardization': lambda d: (d - self.stat['mean'])/np.sqrt(self.stat['var']),
                               'rating': lambda d: (d/5)*2 - 1}
        self.inverse_transform_func = {'normalization': lambda d: d * (self.stat['max'] - self.stat['min']) + self.stat['min'],
                                       'standardization': lambda d: d * np.sqrt(self.stat['var']) + self.stat['mean'],
                                       'rating': lambda d: ((d+1)/2) * 5}
        if transform_func is not None: self.transform_func.update(transform_func)
    def track(self, conn=None, table=None, column=None, db_tracker_mapping=None, 
                    data:pd.Series=None, it_tracker_mapping=None):
        if self.tracker_type == 'db':
            conn = sqlite3.connect(conn)
            db_tracker = {'count': 'count({column})', 'mean': 'avg({column})', 
                          'max': 'max({column})', 'min': 'min({column})', 
                          'var': 'avg({column}*{column}) - avg({column})*avg({column})'}
            if db_tracker_mapping is not None:
                db_tracker.update(db_tracker_mapping)
            for key in db_tracker:
                current_sql = 'select {field} from `{table}`'.format(field=db_tracker[key].format(column=column), table=table)
                self.stat[key] = float(pd.read_sql(current_sql, conn).iloc[0][0])
        if self.tracker_type == 'iterable':
            it_tracker = {'count': 'count', 'mean': 'mean', 'max': 'max', 'min': 'min', 'var': 'var'}
            if it_tracker_mapping is not None:
                it_tracker.update(it_tracker_mapping)
            for key in it_tracker:
                self.stat[key] = eval(f'data.{it_tracker[key]}()')
        super().track()
        return self
    def transform(self, x):
        try:
            output = float(self.transform_func[self.transform_type](x))
        except:
            output = float({'normalization': 0.5, 'standardization': 0}[self.transform_type])
        return output
    def inverse_transform(self, x):
        return self.inverse_transform_func[self.transform_type](x)
    
class CategoricalFeatureTracker(FeatureTracker):
    def __init__(self, transform_type='json', transform_keys=[], **kwargs):
        super().__init__(**kwargs)
        self.transform_type, self.transform_keys = transform_type, transform_keys
        self.embedding = {}
    def track(self, conn=None, table=None, column=None, data:pd.Series=None):
        if self.tracker_type == 'db':
            conn = sqlite3.connect(conn)
            data = pd.read_sql(f'select `{column}` from `{table}`', conn).iloc[:, 0]
        if self.transform_type == 'single_column':
            key_array = data.unique()
            self.stat[column], self.transform_keys = {key_array[i]:i+1 for i in range(len(key_array))}, [column]
            self.inverse_stat[column] = {i+1:key_array[i] for i in range(len(key_array))}
        else:
            for key in self.transform_keys:
                key_array = data[data.map(lambda x: self.validate_value_by_key(x, key))].map(lambda x: self.extract_value_by_key(x, key)).unique()
                self.stat[key] = {key_array[i]:i+1 for i in range(len(key_array))}
                self.inverse_stat[key] = {i+1:key_array[i] for i in range(len(key_array))}
        super().track()
        return self
    def transform(self, x:str):
        res = []
        for key in self.transform_keys:
            if self.transform_type == 'single_column':
                res.append(self.stat[key].get(x, 0))
                break
            if not self.validate_value_by_key(x, key): 
                res.append(0)
            else:
                x_current = self.extract_value_by_key(x, key)
                res.append(self.stat[key].get(x_current, 0))
        return torch.LongTensor(res)
    def inverse_transform(self, x: list):
        res = {}
        for index, key in enumerate(self.transform_keys):
            res[key] = self.inverse_stat[key].get(x[index], None)
        return res

class MultipleCategoricalFeatureTracker(FeatureTracker):
    def __init__(self, transform_type='json', transform_keys=[], reduce='concat', min_len=8, **kwargs):
        super().__init__(**kwargs)
        assert reduce in ['concat', 'avg_pooling']
        self.transform_type, self.transform_keys, self.reduce, self.min_len = transform_type, transform_keys, reduce, min_len
        self.embedding = {}
    def track(self, conn=None, table=None, column=None, data:pd.Series=None):
        if self.tracker_type == 'db':
            conn = sqlite3.connect(conn)
            data = pd.read_sql(f'select `{column}` from `{table}`', conn).iloc[:, 0]
        full = pd.DataFrame(data.map(self.extract_value_list).sum()).drop_duplicates()
        for key in self.transform_keys:
            key_array = full[key].unique()
            self.stat[key] = {key_array[i]:i+1 for i in range(len(key_array))}
            self.inverse_stat[key] = {i+1:key_array[i] for i in range(len(key_array))}
        super().track()
        return self
    def transform(self, x:str):
        res = []
        x_list = self.extract_value_list(x)
        for di in x_list:
            resi = []
            for key in self.transform_keys:
                x_current = di.get(key, None)
                resi.append(self.stat[key].get(x_current, 0))
            res.append(resi)
        res = res[0:self.min_len]
        if len(res) == 0:
            res = [[0 for i in range(len(self.transform_keys))]]
        if len(res) < self.min_len:
            element = [self.default] * len(res[-1])
            append = [element] * (self.min_len-len(res))
            res += append
        return torch.LongTensor(res)
    def inverse_transform(self, x:list):
        res = []
        for i in x:
            current_res = {}
            for index, key in enumerate(self.transform_keys):
                current_res[key] = self.inverse_stat[key].get(i[index], None)
            res.append(current_res)
        return res

class PromptFeatureTracker(FeatureTracker):
    def __init__(self, template=None, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.extract = {
            'genres': lambda x: ', '.join([i['name'] for i in self.extract_value_list(x)]), 
            'release_date': lambda x: x, 
            'title': lambda x: x, 
            'production_companies': lambda x: ', '.join([i['name'] for i in self.extract_value_list(x)]), 
            'production_countries': lambda x: ', '.join([i['name'] for i in self.extract_value_list(x)]), 
            'tagline': lambda x: x,
            'keywords': lambda x: ', '.join([i['name'] for i in self.extract_value_list(x)]), 
            'overview': lambda x: x}
        self.template = """
Movie Title:
    {title}
Genres:
    {genres}
Release Date:
    {release_date}
Production Companies:
    {production_companies}
Production Countries:
    {production_countries}
Keywords:
    {keywords}
Tagline:
    {tagline}
Overview:
    {overview}
"""
    def transform(self, x:dict):
        extraction = {key: self.extract[key](x[key]) for key in self.extract}
        return self.template.format(**extraction)


class RatingDatasetMovie(RatingDataset):
    def __init__(self, fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=None, row_range=[0,1], verbose=False, load_from_path=False):
        super().__init__(fetch_type=fetch_type, rating_table=rating_table, movie_table=movie_table, conn_path=conn_path, row_range=row_range, verbose=verbose, load_from_path=load_from_path)
        self.order = ['revenue', 'budget', 'runtime', 'popularity', 'vote_average', 'vote_count', 'release_date_timestamp', 
                    'adult', 'belongs_to_collection', 'id', 'status', 'have_release_date',
                    'genres', 'spoken_languages', 'production_companies', 'production_countries', 'keywords', 'cast', 'crew','prompt']
        self.order_dict = {k:i for k,i in zip(self.order, range(len(self.order)))}
        self.get_fetch_mapping()

    def get_original_form(self, i, get_row=False):
        mapped_id = self.fetch_mapping[i]
        fetch_cols = '''m.cast, m.crew, m.keywords, m.adult, 
                        m.belongs_to_collection, m.budget, m.genres, m.homepage, 
                        m.id, m.original_language, m.original_title, m.overview, 
                        m.popularity, m.poster_path, m.production_companies, m.production_countries, 
                        m.release_date, m.release_date_timestamp, m.have_release_date, m.revenue, 
                        m.runtime, m.spoken_languages, m.status, 
                        m.tagline, m.title, m.vote_average, m.vote_count'''
        sql = f'''
                select {fetch_cols} from `{self.movie_table}` as m where id = {mapped_id}
                '''
        #conn.execute(sql, row).fetchall()
        if self.conn is None:
            self.build_conn()
        s = pd.read_sql(sql, self.conn).iloc[0]
        if get_row:
            return s, mapped_id
        return s
    def __getitem__(self, i):
        s = self.get_original_form(i)
        res = [self.trackers[k].transform(s[self.trackers[k].including]) for k in self.order]
        return res
    def init_len(self):
        pass
    def get_fetch_mapping(self):
        self.build_conn()
        s = pd.read_sql(f'select distinct `id` from `{self.movie_table}`', self.conn).iloc[:, 0]
        self.fetch_mapping = s.to_dict()
        self.remove_conn()
    def __len__(self):
        if self.conn is None:
            self.build_conn()
        s = pd.read_sql(f'select distinct `id` from `{self.movie_table}`', self.conn).iloc[:, 0]
        return s.index[-1]
            
class RatingDatasetUser(torch.utils.data.Dataset):
    def __init__(self, userId_tracker, fix_timestamp=None):
        self.stat = userId_tracker.stat['userId']
        self.order = list(self.stat.keys())
        self.fix_timestamp = fix_timestamp
    
    def __getitem__(self, i):
        return torch.LongTensor([self.stat[self.order[i]]]), self.fix_timestamp
    
    def __len__(self):
        return len(self.stat)