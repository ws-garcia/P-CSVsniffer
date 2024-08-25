import os
import json

from test_runner import grammar_helper
def generate():
     basePath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'ground truth')
     json_urls = os.path.join(basePath, 'urls_github.json')
     json_ground_truth = os.path.join(basePath, 'out_reference_github.json')
     out_path = os.path.join(basePath, 'CCSV-all_test_files.txt')
     gh = grammar_helper()
     json_url_lines = read_json(json_urls).split('\n')
     json_ground_dict = create_md5_dict(read_json(json_ground_truth).split('\n'))
     csv_out = []
     csv_out.append('#This file contains the dialects for all files from van den Burg 2019.')
     csv_out.append('file_name|encoding|fields_delimiter|quotechar|escapechar|records_delimiter')
     for line in json_url_lines:
          if line != '':
               json_dict = json.loads(line)
               test = json_ground_dict[json_dict['md5']]
               if test['status'] == 'OK':
                    try:
                         csv_row = '|'.join(
                                        [json_dict['urls'][0].split('/')[-1], 
                                        'utf_8',
                                        gh.get_delimiter_name(test['dialect']['delimiter']),
                                        gh.get_quote_name(test['dialect']['quotechar']),
                                        gh.get_escape_char_name(test['dialect']['escapechar']),
                                        'lf']
                                        )
                         csv_out.append(csv_row)
                    except Exception as e:
                         pass
     write_to_file(out_path,'\r\n'.join(csv_out))

def read_json(full_path: str)-> str:
     with open(full_path, newline='') as jsonfile:
          json_data = jsonfile.read()
          jsonfile.close
          return json_data

def write_to_file(full_path: str, data: str)-> None:
     with open(full_path, 'w', newline='') as textfile:
          textfile.write(data)
          textfile.close  

def create_md5_dict(_dialects_lines: dict)->dict:
     _tmp_dict = {}
     for line in _dialects_lines:
          if  line != '':
               json_dict = json.loads(line)
               md5 = json_dict['filename'].split('/')[-1][:-4]
               _tmp_dict[md5] = json_dict
     return _tmp_dict
if __name__ == "__main__":
     '''
     _dict = '{\
               "detector": "reference", \
               "filename": "./data/github/000b4f49c81221ce738f5b6508808d87.csv", \
               "hostname": "archlinux", \
               "runtime": "null", \
               "status": "OK", \
               "dialect": {"delimiter": ",", "quotechar": "", "escapechar": ""}, \
               "original_detector": "human"}'
     arr_ = [_dict]
     print(create_md5_dict(arr_))
     '''
     generate() 