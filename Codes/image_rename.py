import os
from tqdm import tqdm

path = 'Car_Num_Plate_Detection\\Data\\archive\\images'
files = os.listdir(path)

max_len = len(str(len(files)))
print(max_len)

for i, file in (enumerate(tqdm(files, desc='Renaimg...'))):
    ext = '.' + file.split('.')[-1]
    name = '0' * (max_len - len(str(i))) + str(i)
    new_file_name = name + ext
    os.rename(os.path.join(path, file), os.path.join(path, new_file_name))
