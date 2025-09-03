module ConfigManager

using YAML
using Serialization
using CSV
using DataFrames
using Plots

# Load environment variables from .env file (manually, since DotEnv.load() is not available)
if isfile(".env")
    for line in eachline(".env")
        m = match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$", line)
        if m !== nothing
            ENV[m.captures[1]] = strip(replace(m.captures[2], "\"" => ""))
        end
    end
end
const DATA_PATH = ENV["DATA_PATH"]

export load_configs, save_configs, initialise_config, save_figure, save_data, clear_data_and_figure, print_config, load_data

"""
    load_configs(folder_name::String, config_suffix::String="v1") -> Dict

Load a YAML configuration file.
"""
function load_configs(folder_name::String, config_suffix::String="v1")::Dict
    config_path = joinpath(DATA_PATH, folder_name, "config_$(config_suffix).yml")
    return YAML.load_file(config_path)
end

"""
    save_configs(folder_name::String, config::Dict, config_suffix::String="v1")

Save a dictionary to a YAML configuration file.
"""
function save_configs(folder_name::String, config::Dict, config_suffix::String="v1")
    config_path = joinpath(DATA_PATH, folder_name, "config_$(config_suffix).yml")
    YAML.write_file(config_path, config)
end

"""
    initialise_config(folder_name::String; verbose::Int=0)

Create a folder and set up the initial experimental structure (data and figures subfolders).
"""
function initialise_config(folder_name::String; verbose::Int=0)
    folder_path = joinpath(DATA_PATH, folder_name)
    if !isdir(folder_path)
        mkpath(joinpath(folder_path, "data"))
        mkpath(joinpath(folder_path, "figures"))
        if verbose > 0
            println("Created folder structure at $folder_path")
        end
    else
        if verbose > 0
            println("Folder $folder_path already exists. No changes made.")
        end
    end
end

"""
    save_figure(notebook_config::Dict, fig, fig_name::String; fig_format::String="png", verbose::Int=0, kwargs...)

Save a plot to the figures directory.
"""
function save_figure(notebook_config::Dict, fig, fig_name::String; fig_format::String="png", verbose::Int=0, kwargs...)
    folder_name = notebook_config["name"]
    config_version = get(notebook_config, "version", "v1")
    figures_path = joinpath(DATA_PATH, folder_name, "figures")
    mkpath(figures_path)
    fig_path = joinpath(figures_path, "$(config_version)_$(fig_name).$(fig_format)")
    savefig(fig, fig_path; kwargs...)
    
    if verbose > 0
        println("Figure saved at $fig_path")
    end
end

"""
    save_data(notebook_config::Dict, data, data_name::String; data_format::String="jls", verbose::Int=0, kwargs...)

Saves data to the data directory. Supports Julia serialization (.jls) and CSV (.csv) for DataFrames.
"""
function save_data(notebook_config::Dict, data, data_name::String; data_format::String="jls", verbose::Int=0, kwargs...)
    folder_name = notebook_config["name"]
    config_version = get(notebook_config, "version", "v1")
    data_path = joinpath(DATA_PATH, folder_name, "data")
    mkpath(data_path)
    data_file_path = joinpath(data_path, "$(config_version)_$(data_name).$(data_format)")

    if data_format == "jls"
        serialize(data_file_path, data)
    elseif data_format == "csv"
        if data isa DataFrame
            CSV.write(data_file_path, data; kwargs...)
        else
            error("Data is not a DataFrame, cannot save as CSV.")
        end
    else
        error("Unsupported data format. Use 'jls' or 'csv'.")
    end

    if verbose > 0
        println("Data saved at $data_file_path")
    end
end

"""
    clear_data_and_figure(notebook_config::Dict; data::Bool=true, figure::Bool=true, verbose::Int=0)

Clears all data and figures for a specific configuration version.
"""
function clear_data_and_figure(notebook_config::Dict; data::Bool=true, figure::Bool=true, verbose::Int=0)
    if !data && !figure
        if verbose > 0
            println("No action taken. Both data and figure flags are set to false.")
        end
        return
    end

    folder_name = notebook_config["name"]
    config_version = get(notebook_config, "version", "v1")

    if data
        data_path = joinpath(DATA_PATH, folder_name, "data")
        if isdir(data_path)
            for file in readdir(data_path)
                if startswith(file, config_version * "_")
                    rm(joinpath(data_path, file))
                end
            end
            if verbose > 0
                println("Cleared data files for version $config_version in $data_path")
            end
        end
    end

    if figure
        figures_path = joinpath(DATA_PATH, folder_name, "figures")
        if isdir(figures_path)
            for file in readdir(figures_path)
                if startswith(file, config_version * "_")
                    rm(joinpath(figures_path, file))
                end
            end
            if verbose > 0
                println("Cleared figure files for version $config_version in $figures_path")
            end
        end
    end
end

"""
    print_config(d::Dict, indent=0)

Recursively prints the contents of a dictionary.
"""
function print_config(d::Dict, indent=0)
    for (key, value) in d
        print(" " ^ indent, key, ": ")
        if value isa Dict
            println()
            print_config(value, indent + 2)
        else
            println(value)
        end
    end
end

"""
    load_data(notebook_config::Dict, data_name::String; data_format::String="jls", verbose::Int=0, kwargs...) -> Any

Loads data from the data directory.
"""
function load_data(notebook_config::Dict, data_name::String; data_format::String="jls", verbose::Int=0, kwargs...)::Any
    folder_name = notebook_config["name"]
    config_version = get(notebook_config, "version", "v1")
    data_path = joinpath(DATA_PATH, folder_name, "data")
    data_file_path = joinpath(data_path, "$(config_version)_$(data_name).$(data_format)")

    if !isfile(data_file_path)
        error("Data file not found: $data_file_path")
    end

    local data
    if data_format == "jls"
        data = deserialize(data_file_path)
    elseif data_format == "csv"
        data = CSV.read(data_file_path, DataFrame; kwargs...)
    else
        error("Unsupported data format. Use 'jls' or 'csv'.")
    end

    if verbose > 0
        println("Data loaded from $data_file_path")
    end

    return data
end

end # module ConfigManager
