import os
import yaml
import dotenv
import matplotlib.pyplot as plt
import pickle
import pandas as pd

dotenv.load_dotenv()
new_path = os.getenv("NEW_DATA_PATH")

def load_configs(folder_name: str, config_suffix: str = "v1") -> dict:
    config_path = os.path.join(new_path, folder_name, f"config_{config_suffix}.yml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)  # Use safe_load to prevent code execution
    return config

def save_configs(folder_name: str, config: dict, config_suffix: str = "v1") -> None:
    config_path = os.path.join(new_path, folder_name, f"config_{config_suffix}.yml")
    with open(config_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)  # sort_keys=False to maintain order
        
def initialise_config(folder_name: str, verbose: int = 0) -> None:
    '''
    Create a folder and set-up the initial experimental structure
    '''
    folder_path = os.path.join(new_path, folder_name)
    # check if folder exists, if not create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        # make 'data' and 'figures' subfolders
        os.makedirs(os.path.join(folder_path, 'data'), exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'figures'), exist_ok=True)
        if verbose > 0:
            print(f"Created folder structure at {folder_path}")
    else: 
        if verbose > 0:
            print(f"Folder {folder_path} already exists. No changes made.")
        
    
def save_figure(notebook_config: dict, fig: plt.Figure, fig_name: str, fig_format: str = "png", verbose: int = 0, **kwargs) -> None:
    '''
    notebook_config: dict
        The configuration dictionary containing the folder name.
        The folder name is accessible via notebook_config['name'].
        The config version is accessible via notebook_config['version'].
    fig: plt.Figure
        The matplotlib figure to be saved.
    fig_name: str
        The name of the figure file (without extension).
    fig_format: str
        The format to save the figure in (default is 'png').
    **kwargs:
        Additional keyword arguments to pass to fig.savefig().
    '''
    folder_name = notebook_config['name']
    config_version = notebook_config.get('version', 'v1') # Default to 'v1' if not specified
    figures_path = os.path.join(new_path, folder_name, 'figures')
    if not os.path.exists(figures_path):
        os.makedirs(figures_path, exist_ok=True)
    fig_path = os.path.join(figures_path, f"{config_version}_{fig_name}.{fig_format}")
    fig.savefig(fig_path, format=fig_format, **kwargs)
    
    if verbose > 0:
        print(f"Figure saved at {fig_path}")
        
    
def save_data(notebook_config: dict, data: any, data_name: str, data_format: str = 'pkl', verbose: int = 0, **kwargs) -> None:
    '''
    Saves data as a pickled file in the appropriate data folder.
    If the data is a pandas DataFrame and <1000 rows and columns, it is also saved as a CSV file.
    notebook_config: dict
        The configuration dictionary containing the folder name.
        The folder name is accessible via notebook_config['name'].
        The config version is accessible via notebook_config['version'].
    data: any
        The data to be saved. Should have a 'to_csv' method if saving as CSV.
    data_name: str
        The name of the data file (without extension).
    **kwargs:
        Additional keyword arguments to pass to the data saving method.
    '''
    folder_name = notebook_config['name']
    config_version = notebook_config.get('version', 'v1') # Default to 'v1' if not specified
    data_path = os.path.join(new_path, folder_name, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path, exist_ok=True)
    data_file_path = os.path.join(data_path, f"{config_version}_{data_name}.{data_format}")
    if data_format == 'pkl':
        with open(data_file_path, 'wb') as f:
            pickle.dump(data, f, **kwargs)
    elif data_format == 'csv':
        if hasattr(data, 'to_csv'):
            data.to_csv(data_file_path, **kwargs)
        else:
            raise ValueError("Data does not have a 'to_csv' method.")
    else:
        raise ValueError("Unsupported data format. Use 'pkl' or 'csv'.")
    
    if verbose > 0:
        print(f"Data saved at {data_file_path}")
    

def clear_data_and_figure(notebook_config: dict, data: bool = True, figure: bool = True, verbose: int = 0) -> None:
    '''
    Clears all data and figures for a specific configuration version.
    notebook_config: dict
        The configuration dictionary containing the folder name.
        The folder name is accessible via notebook_config['name'].
        The config version is accessible via notebook_config['version'].
    data: bool
        If True, clears data files.
    figure: bool
        If True, clears figure files.
    '''
    
    if not data and not figure:
        if verbose > 0:
            print("No action taken. Both data and figure flags are set to False.")
        return
    
    folder_name = notebook_config['name']
    config_version = notebook_config.get('version', 'v1') # Default to 'v1' if not specified
    
    # Clear data files
    data_path = os.path.join(new_path, folder_name, 'data')
    if os.path.exists(data_path):
        for file in os.listdir(data_path):
            if file.startswith(config_version + "_"):
                os.remove(os.path.join(data_path, file))
        if verbose > 0:
            print(f"Cleared data files for version {config_version} in {data_path}")
    
    # Clear figure files
    figures_path = os.path.join(new_path, folder_name, 'figures')
    if os.path.exists(figures_path):
        for file in os.listdir(figures_path):
            if file.startswith(config_version + "_"):
                os.remove(os.path.join(figures_path, file))
        if verbose > 0:
            print(f"Cleared figure files for version {config_version} in {figures_path}")
            
def print_config(d, indent=0):
    for key, value in d.items():
        print(" " * indent + str(key) + ":", end=" ")
        if isinstance(value, dict):
            print()
            print_config(value, indent + 2)
        else:
            print(str(value))

def load_data(notebook_config: dict, data_name: str, data_format: str = 'pkl', verbose: int = 0, **kwargs) -> any:
    '''
    Loads data from the appropriate data folder.
    notebook_config: dict
        The configuration dictionary containing the folder name.
        The folder name is accessible via notebook_config['name'].
        The config version is accessible via notebook_config['version'].
    data_name: str
        The name of the data file (without extension).
    data_format: str
        The format of the data file ('pkl' or 'csv').
    **kwargs:
        Additional keyword arguments to pass to the data loading method.
    Returns:
        The loaded data.
    '''
    folder_name = notebook_config['name']
    config_version = notebook_config.get('version', 'v1') # Default to 'v1' if not specified
    data_path = os.path.join(new_path, folder_name, 'data')
    data_file_path = os.path.join(data_path, f"{config_version}_{data_name}.{data_format}")
    
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"Data file not found: {data_file_path}")
    
    if data_format == 'pkl':
        with open(data_file_path, 'rb') as f:
            data = pickle.load(f, **kwargs)
    elif data_format == 'csv':
        data = pd.read_csv(data_file_path, **kwargs)
    else:
        raise ValueError("Unsupported data format. Use 'pkl' or 'csv'.")
    
    if verbose > 0:
        print(f"Data loaded from {data_file_path}")
    
    return data
