import sqlite3
import pandas as pd
import numpy as np
from dataset import RatingDataset, FeatureTracker, NumericalFeatureTracker, CategoricalFeatureTracker, MultipleCategoricalFeatureTracker, PromptFeatureTracker
from model import FusionModel
from torch.cuda.amp import autocast, GradScaler
from torch.utils.tensorboard import SummaryWriter
import torch
import dill as pickle
import os
import json

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

def is_int(x):
    try:
        int(x)
        return True
    except:
        return False

def extract_timestamp(date, mean):
    try: return pd.to_datetime(date).timestamp()
    except: return mean

if __name__ == '__main__':
    WRITE_DATA = True
    BUILD_DS = True
    data_path = 'data'
    #######################################################################################
    #### 1. Data Pre-processing
    #######################################################################################
    print('1. Data Pre-processing')
    if WRITE_DATA:
        links = pd.read_csv(f'{data_path}/links.csv', encoding='utf8', low_memory=False).rename(columns={'tmdbId': 'id'}).dropna(subset=['id'])
        links['id'] = links['id'].astype(int)

        credits = pd.read_csv(f'{data_path}/credits.csv', encoding='utf8', low_memory=False)
        keywords = pd.read_csv(f'{data_path}/keywords.csv', encoding='utf8', low_memory=False)
        movies_metadata = pd.read_csv(f'{data_path}/movies_metadata.csv', encoding='utf8', low_memory=False)

        movies_metadata = movies_metadata[movies_metadata.id.map(is_int)]
        movies_metadata['id'] = movies_metadata['id'].astype(int)
        for n in ['popularity', 'budget', 'revenue', 'budget', 'runtime', 'popularity', 'vote_average', 'vote_count']:
            try:
                movies_metadata[n] = movies_metadata[n].fillna(0).astype(int)
            except:
                movies_metadata[n] = movies_metadata[n].fillna(0).astype(float)
        mean_timestamp = pd.to_datetime(movies_metadata['release_date']).mean().timestamp()
        movies_metadata['release_date_timestamp'] = movies_metadata['release_date'].map(
                                                lambda x: extract_timestamp(x, mean_timestamp))
        movies_metadata['have_release_date'] = movies_metadata['release_date'].isna().map(lambda x: str(x))

        ratings = pd.read_csv(f'{data_path}/ratings.csv', low_memory=False)
        ratings = ratings.merge(links[['movieId', 'id']], on='movieId', how='left')
        credits = credits.set_index('id')
        keywords = keywords.set_index('id')
        movies_metadata = movies_metadata.merge(keywords, on='id', how='left').merge(credits, on='id', how='left')
        movies_metadata = movies_metadata.drop_duplicates().reset_index()
        movies_metadata = movies_metadata.set_index('id')
        ratings = ratings.dropna(subset=['id'])
        ratings['id'] = ratings['id'].astype(int)
        ratings = ratings.drop_duplicates().reset_index()
        ratings.index = ratings.index.set_names('row_id')

    #######################################################################################
    #### 2. Database Connection
    #######################################################################################
    print('2. Database Connection')
    conn_path = 'dataset.db'
    external_conn = sqlite3.connect(conn_path)
    if WRITE_DATA:
        movies_metadata.to_sql('movies', external_conn, if_exists='replace', index=True)
        ratings.to_sql('ratings', external_conn, if_exists='replace', index=True)
        external_conn.execute('CREATE INDEX movies_id_index ON movies (id);')
        external_conn.execute('CREATE INDEX ratings_row_id_index ON ratings (row_id);')

    #######################################################################################
    #### 3. Build Assets for Model Training
    #######################################################################################
    print('3. Build Assets for Model Training')
    MIXEDPRECISION = True
    if BUILD_DS:
        ds = RatingDataset(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0, 0.8], verbose=False, load_from_path=False)
        ds.save('ds.pkl')
        ds_test = RatingDataset(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0.8, 1], verbose=False, load_from_path=False)
        ds_test.save('ds_test.pkl')
    else:
        ds = RatingDataset(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0, 0.8], verbose=False, load_from_path="ds.pkl")
        ds_test = RatingDataset(fetch_type='db', rating_table='ratings', movie_table='movies', conn_path=conn_path, row_range=[0.8, 1], verbose=False, load_from_path="ds_test.pkl")
    padding_idx = 0
    with open('embedding_configs.json') as f:
        embedding_configs = json.load(f)
    BATCH_SIZE = 128
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    train_data = torch.utils.data.DataLoader(ds, 
                                            batch_size=BATCH_SIZE, 
                                            num_workers=0,
                                            shuffle=True,
                                            pin_memory=True,
                                            prefetch_factor = 2,
                                            drop_last=True
                                            )
    test_data = torch.utils.data.DataLoader(ds, 
                                            batch_size=2*BATCH_SIZE, 
                                            num_workers=0,
                                            shuffle=True,
                                            pin_memory=False
                                            )
    model = FusionModel(ds=ds, output_len = 128, embedding_configs=embedding_configs, avgpooling_output_len = 128, text_encoder_output_len = 128)
    try:
        model.load_state_dict(torch.load('model_image.pkl'))
        print(f'Model Parameters Loaded from "model_image.pkl"')
    except:
        print(f'Model Parameters Initialized')
    if torch.cuda.is_available():
        model = model.cuda()
    else:
        model = model.cpu()

    scaler = GradScaler(enabled=MIXEDPRECISION)

    epochs = 100
    restart_lr = 0.00015
    lr_penalty_rate = 0.999985
    accumulate = 2
    total_steps = int(((len(ds) // BATCH_SIZE) * epochs)/accumulate)
    optimizer = torch.optim.Adam(model.parameters(), lr = restart_lr, eps = 1e-5)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, lr_penalty_rate)
    optimizer.zero_grad()
    count = 0
    writer = SummaryWriter()
    losses = []
    losses_test = []

    #######################################################################################
    #### 4. Model Training
    #######################################################################################
    print('4. Model Training')
    for epoch in range(epochs):
        for index, d in enumerate(train_data):
            for ic in range(len(d[0])):
                try:
                    d[0][ic] = d[0][ic].to(device)
                except Exception as e:
                    # print(e, end=' ')
                    pass
            d[1] = d[1].float().to(device)

            with autocast(enabled=MIXEDPRECISION):
                mse = model(d, external_loss_calculation=False)

            scaler.scale(mse).backward()
            if count % accumulate == 0 and count != 0:
                # optimizer.step()
                scaler.step(optimizer)
                scheduler.step()
                optimizer.zero_grad()
                scaler.update()

            if count % 100 == 0:
                del d
                for index2, d2 in enumerate(test_data):
                    for ic in range(len(d2[0])):
                        try:
                            d2[0][ic] = d2[0][ic].to(device)
                        except Exception as e:
                            pass
                    d2[1] = d2[1].float().to(device)
                    model.eval()
                    with autocast(enabled=MIXEDPRECISION):

                        mse2 = model(d2, external_loss_calculation=False)

                    model.train()
                    losses_test.append(float(mse2))
                    break
                del d2
            losses.append(float(mse))

            writer.add_scalar('Training/LR', float(scheduler.get_last_lr()[0]), count)
            writer.add_scalar('Training/Epoch', float(epoch), count)
            writer.add_scalar('Loss/TrainLoss', float(mse), count)
            writer.add_scalar('Loss/TestLoss', float(mse2), count)

            if count % 200 == 0:
                closs = losses[-99:]
                loss_display = ["{:.4f}".format(i) for i in [np.min(closs), np.quantile(closs, 0.25), np.mean(closs), np.quantile(closs, 0.75), np.max(closs)]]
                closs = losses_test[-99:]
                loss_display_test = ["{:.4f}".format(i) for i in [np.min(closs), np.quantile(closs, 0.25), np.mean(closs), np.quantile(closs, 0.75), np.max(closs)]]
                print(f'Current Index:({count}, {index}, {epoch}), Tracking: {loss_display}, Tracking: {loss_display_test}')
            if index % 2000 == 0 and index != 0:
                torch.save(model.state_dict(), f'model_image.pkl')
            count += 1
    
