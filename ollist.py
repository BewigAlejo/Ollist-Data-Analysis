import kagglehub
#import pandas as pd
import os
# kagglehub.login()

path = kagglehub.dataset_download(
    "olistbr/brazilian-ecommerce"
)

print("Path to dataset files:", path)