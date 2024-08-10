import time
import json
import zipfile
import streamlit as st


def check_for_biome_folders(zip_file):
    global start
    start = time.time()
    with zipfile.ZipFile(zip_file, 'r') as myzip:
        root = zipfile.Path(myzip)
        contents = myzip.namelist()
        data_folders = [f for f in contents if f.startswith('data/') and f.endswith('/')]
        biome_folders = []
        for folder in data_folders:
            folder_contents = myzip.namelist()
            biome_folder = folder + "worldgen/biome/"
            if biome_folder in folder_contents and "/tags/" not in folder:
                biome_folders.append(biome_folder)
        global end
        end = time.time()
        return biome_folders


def create_json_file(zip_files):
  biome_data = {}

  for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, 'r') as myzip:
      folder_contents = myzip.namelist()
      biome_files = [f for f in folder_contents if f.startswith('data/') and not f.endswith('/') and f.endswith('.json') and "biome/" in f and "/tags/" not in f]

      for f in biome_files:
        json_name = f.split("/")[-1].replace(".json", "")
        namespace_name = f.split("/")[-4].split("/")[-1]
        biome_data[f"biome.{namespace_name}.{json_name}"] = json_name.replace("_", " ").title()
        return biome_data


def main():
    st.set_page_config(page_title="Biome Name Fix", page_icon="🏝️")
    st.write("""
      # Biome Name Fix Generator
      
      When using datapacks that add new biomes, you may notice that mods such as Xaero's Minimap, Journeymap, and MiniHUD display untranslated biome names as 'biome.namespace.biomename,' which isn't very pretty.

      This tool solves that issue by generating a language file that you can place in a [resource pack](https://minecraft.wiki/w/Resource_pack#Language) or mod.
    """)
    st.image('https://i.postimg.cc/YSZv9z51/bnf.png', use_column_width='always')
    files = st.file_uploader("Upload a datapack or mod", type=["zip", "jar"], accept_multiple_files=True)

    biome_folders = []
    if files:
      for file in files:
        if file is not None:
          folders = check_for_biome_folders(file)
          for f in folders:
            biome_folders.append(f)

      if len(biome_folders) > 0:
        st.info("Biomes were found in the following locations:")
        for folder in biome_folders:
          st.write(folder)
        st.caption("Parsed in " + str(int((end - start)*1000)) + "ms")
        json_data = create_json_file(files)
        st.download_button("Download JSON file", json.dumps(json_data, indent=2), file_name="en_us.json", type="primary")
      else:
        st.error("No biomes were found.")


if __name__ == "__main__":
    main()
