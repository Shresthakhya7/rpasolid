from RPA.Excel.Files import Files


class ExcelFile():
    def __init__(self):
          self.excel=Files()

    def read_movie_list_from_excel(self):
            self.excel.open_workbook("Movies.xlsx")
            movie_list=self.excel.read_worksheet_as_table(header=True)
            self.excel.close_workbook()
        
            return [movie['Movie'] for movie in movie_list]
    
    def close_excel(self):
          self.excel.close_workbook()
          print("File Closed")
    