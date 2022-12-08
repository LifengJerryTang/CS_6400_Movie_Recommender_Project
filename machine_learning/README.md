## Movie Recommendation Model
This recommendation model is built using PyTorch and the Transformers library in Python. It is designed to predict items that a user may be interested in based on their previous interactions (rating activities) with the movie items.

### Getting Started
##### Prerequisites
To run this project, you will need Python 3 and the following libraries:
- dill
- einops
- einops_exts
- numpy
- pandas
- torch
- transformers

Use the requirements.txt to prepare the pytorch development environment. Note that if you are using pytorch without GPU, you need to delete the ```+cu113``` from the line of ```torch==1.10.0+cu113``` in the requirement file.  
```python
pip install -r requirements.txt
```

Before running the training and sampling scripts, you need to first download the TMDB dataset used in this model from [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and put the csv files into a directory named as data ```(./data/xxx.csv)```. 

### Usage
To train the model, run the following command:
```python
python -u train.py
```
It will take some time to initialize the dataset and the intermediate results of data preparing will be saved in the files including ```dataset.db```, ```ds.pkl``` and ```ds_test.pkl```. When you need to resume the training or run the code for a second time, you can change the variables ```WRITE_DATA``` and ```BUILD_DS``` to ```False``` in the ```train.py``` in order to shorten the time for data preparing. In the production environment, when the data source is extracted with ETL daily or hourly, we can change these two variables correspondingly after the new data extraction to update the data trackers saved in the ```ds.pkl```. 

The model image checkpoint will be saved in the file ```model_image.pkl``` once 2000 steps of training. To use the model parameters for inference, load the model parameter after initializing the ```FusionModel``` class imported from ```model.py``` and use the ```FusionModel.calculate_user_feature()``` method to do the prediction. Please follow the steps in ```calculate.py``` for vector representation calculation. To calculate the movie and user representation for the full dataset, simply run
```python
python -u calculate.py
```
The calculated representation results will be stored in ```movie_feature_calculated.csv``` and ```user_feature_calculated.csv```. 

## References

- [Transformers library](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)

```
# Recommendation System Structure: about Semantic Model, Negative Sampling, and Contrastive Learning
[1] Huang, P. S., He, X., Gao, J., Deng, L., Acero, A., & Heck, L. (2013, October). Learning deep structured semantic models for web search using clickthrough data. In Proceedings of the 22nd ACM international conference on Information & Knowledge Management (pp. 2333-2338).
[2] Covington, P., Adams, J., & Sargin, E. (2016, September). Deep neural networks for youtube recommendations. In Proceedings of the 10th ACM conference on recommender systems (pp. 191-198).
[3] Huang, J. T., Sharma, A., Sun, S., Xia, L., Zhang, D., Pronin, P., ... & Yang, L. (2020, August). Embedding-based retrieval in facebook search. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2553-2561).
[4] Yi, X., Yang, J., Hong, L., Cheng, D. Z., Heldt, L., Kumthekar, A., ... & Chi, E. (2019, September). Sampling-bias-corrected neural modeling for large corpus item recommendations. In Proceedings of the 13th ACM Conference on Recommender Systems (pp. 269-277).
# Sequential Feature Encoder: Transformer, Perceiver Attention, Perceiver Resampler
[6] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in neural information processing systems, 30.
[7] Jaegle, A., Gimeno, F., Brock, A., Vinyals, O., Zisserman, A., & Carreira, J. (2021, July). Perceiver: General perception with iterative attention. In International conference on machine learning (pp. 4651-4664). PMLR.
[8] Jaegle, A., Borgeaud, S., Alayrac, J. B., Doersch, C., Ionescu, C., Ding, D., ... & Carreira, J. (2021). Perceiver io: A general architecture for structured inputs & outputs. arXiv preprint arXiv:2107.14795.
# Pretrained Language Model for the Text Encoder: Frozen T5
[9] Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., ... & Liu, P. J. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer. J. Mach. Learn. Res., 21(140), 1-67.
```