import pandas as pd

def load_csv_files(filepaths):
            try:
                data = {}
                for path in filepaths:
                    df = pd.read_csv(path, index_col=0)
                    data[path] = df
                    
                return data
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
            
oli = load_csv_files(['/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Xmas.csv'])

print(oli)