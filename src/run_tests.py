import os
import sys
import platform

from test_runner import runner

def get_results_base_path(basePath:str)->str:
     sys_name = platform.platform(aliased=True,terse=True)
     return os.path.join(basePath, 'tests results', sys_name)

def runsingleTest(threshold: int, \
                  data_threshold: int, \
                    detector: str, \
                    heavy_tests: bool = False)->dict:
     basePath = os.path.dirname(os.path.dirname(__file__))
     limit = threshold  if detector == 'CSVsniffer' else data_threshold
     fw = 'All' if limit == -1 else limit
     pw = "records" if detector == 'CSVsniffer' else "characters"
     formated_sufix = '%r-%r %r loaded' %(detector, fw, pw)
     formated_sufix = formated_sufix.replace("'",'')
     out_path = os.path.join(get_results_base_path(basePath), formated_sufix)
     tmp_result = {}
     if not os.path.exists(out_path):
          os.makedirs(out_path)
     _runner = runner(ground_truth_csv=None,
                      output_path=out_path,
                      delimiter_list=[',', ';', '\t','|', ':', '=', ' ', '#', '*', '%', '^', '&'],
                      quotechar_list=['"', "'", '~', '`'], 
                      expected_results=None,
                      threshold=limit,
                      sniffer=detector,
                      data_threshold=limit)
     if heavy_tests:
          tmp_result[detector] = _runner.run(base_path=basePath,
                                        output_file_names=['[POLLOCK]_output.txt',
                                                       '[W3C-CSVW]_output.txt',
                                                       '[CSV Wrangling]_output.txt',
                                                       '[CSV Wrangling (no codec issues)-ONLY MESSY= False]_output.txt', 
                                                       '[CSV Wrangling (no codec issues)-ONLY MESSY= True]_output.txt',
                                                       '[CSV Wrangling (All test files)]_output.txt',
                                                       '[CSV Wrangling (All Messy test files)]_output.txt'],
                                        expected_results_csv_names=['POLLOCK-dialect_annotations.txt',
                                                                      'W3C-CSVW-dialect_annotations.txt',
                                                                      'CCSV-manual_Dialect_Annotation.txt',
                                                                      'CCSV-manual_Dialect_Annotation_CODEC.txt',
                                                                      'CCSV-manual_Dialect_Annotation_CODEC.txt',
                                                                      'CCSV-all_test_files.txt',
                                                                      'CCSV-all-Messy_test_files.txt'],
                                        test_sets=['CSV', 
                                                  'W3C-CSVW', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling_All',
                                                  'CSV_Wrangling_All']
                                        )
     else:
          tmp_result[detector] = _runner.run(base_path=basePath,
                                        output_file_names=['[POLLOCK]_output.txt',
                                                       '[W3C-CSVW]_output.txt',
                                                       '[CSV Wrangling]_output.txt',
                                                       '[CSV Wrangling (no codec issues)-ONLY MESSY= False]_output.txt', 
                                                       '[CSV Wrangling (no codec issues)-ONLY MESSY= True]_output.txt'],
                                        expected_results_csv_names=['POLLOCK-dialect_annotations.txt',
                                                                      'W3C-CSVW-dialect_annotations.txt',
                                                                      'CCSV-manual_Dialect_Annotation.txt',
                                                                      'CCSV-manual_Dialect_Annotation_CODEC.txt',
                                                                      'CCSV-manual_Dialect_Annotation_CODEC.txt'],
                                        test_sets=['CSV', 
                                                  'W3C-CSVW', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling', 
                                                  'CSV_Wrangling_All']
                                        )
     return tmp_result
if __name__ == "__main__":
     r_base_path = get_results_base_path(os.path.dirname(os.path.dirname(__file__)))
     r_dict = {}
     global_summary = {}
     r_dict['CSVsniffer'] = runsingleTest(threshold=10, # Load 10 records
                   data_threshold=-1, 
                   detector='CSVsniffer',
                   heavy_tests=True) 
     r_dict['CSVsniffer'] = runsingleTest(threshold=50, # Load 50 records
                   data_threshold=-1, 
                   detector='CSVsniffer',
                   heavy_tests=True) 
     r_dict['CleverCSV'] = runsingleTest(threshold=-1, 
                   data_threshold=6144,   # Load 6144 characters
                    detector='CleverCSV', 
                    heavy_tests=True)
     r_dict['Python sniffer'] = runsingleTest(threshold=-1, 
                   data_threshold=6144,   # Load 6144 characters
                    detector='Python sniffer', 
                    heavy_tests=True)
     r_dict['CleverCSV'] = runsingleTest(threshold=-1, 
                   data_threshold=-1,   # Load all file
                    detector='CleverCSV', 
                    heavy_tests=True)
     for key in r_dict:
          sniffers_ = r_dict[key]
          for x in sniffers_:
               n, tc, ptr, delr, fr, et, tp, fp, fn, p, r, f1, wf1 = \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
               summary_dict = {}
               data_sets_results = sniffers_[x]
               for data_set in data_sets_results:
                    n += 1
                    tc += data_sets_results[data_set]['tests count']
                    ptr +=data_sets_results[data_set]['passed ratio']
                    delr += data_sets_results[data_set]['delimiter ratio']
                    fr += data_sets_results[data_set]['failure ratio']
                    et += data_sets_results[data_set]['time']
                    tp += data_sets_results[data_set]['tp']
                    fp += data_sets_results[data_set]['fp']
                    fn += data_sets_results[data_set]['fn']
                    p += data_sets_results[data_set]['precision']
                    r += data_sets_results[data_set]['recall']
                    f1 += data_sets_results[data_set]['f1 score']
                    wf1 += data_sets_results[data_set]['weighted f1 score']
               summary_dict['detector'] = x
               summary_dict['tests count'] = tc
               summary_dict['passed ratio'] = ptr/n
               summary_dict['delimiter ratio'] = delr/n
               summary_dict['failure ratio'] = fr/n
               summary_dict['time'] = et
               summary_dict['tp'] = tp
               summary_dict['fp'] = fp
               summary_dict['fn'] = fn
               summary_dict['precision'] = p/n
               summary_dict['recall'] = r/n
               summary_dict['f1 score'] = f1/n
               summary_dict['weighted f1 score'] = wf1/tp
               global_summary[x] = summary_dict
     sys.stdout = open(os.path.join(r_base_path,'SUMMARY.json'), 'w')
     for x in global_summary:
          print(global_summary[x])
     sys.stdout.close()
