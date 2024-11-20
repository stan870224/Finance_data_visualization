import os

def data_save():
    data_dir = 'D:' + os.path.sep + 'AI_course' + os.path.sep + 'Finance_data_visualization' + os.path.sep + 'Finance_data_visualization' + os.path.sep +'finance_data'
    file_path = 'D:' + os.path.sep + 'AI_course' + os.path.sep + 'Finance_data_visualization' + os.path.sep + 'Finance_data_visualization' + os.path.sep+'top_market_cap_by_sector'
    output_file = os.path.join(file_path,'top_market_cap_by_sector.csv')
    input_file = os.path.join(file_path,'top_market_cap_by_sector.csv')
    table_name = 'Stock_Historical_Data'
    
    return data_dir, file_path, output_file, input_file, table_name