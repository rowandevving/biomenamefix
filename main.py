import time
import json
import os
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


def create_json_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as myzip:
        folder_contents = myzip.namelist()
        biome_files = [f for f in folder_contents if f.startswith('data/') and not f.endswith('/') and f.endswith('.json') and "biome/" in f and "/tags/" not in f]
        biome_data = {}
        for f in biome_files:
            json_name = f.split("/")[-1].replace(".json", "")
            namespace_name = f.split("/")[-4].split("/")[-1]
            biome_data[f"biome.{namespace_name}.{json_name}"] = json_name.replace("_", " ").title()
        with open("en_us.json", "w") as outfile:
            json.dump(biome_data, outfile, indent=2)


def main():
    st.set_page_config(page_title="Biome Name Fix", page_icon="🏝️")
    st.title("Biome Name Fix Generator")
    st.write("You may have noticed that when you play with datapacks that add biomes e.g. Terralith, that mods like Xaero's minimap, Journeymap, MiniHUD and other mods that read biome names have untranslated strings, often looking something like 'biome.namespace.biomename', which is not all that pretty. This tool fixes that by generating a lang file that you can use in the /assets/minecraft/lang folder of a resourcepack or mod. If you wish to make fixes for multiple packs, you can use https://weld.smithed.dev to make a combined pack and then stick it back in here.")
    st.write("See this image as an example:")
    st.image('https://i.postimg.cc/YSZv9z51/bnf.png', use_column_width='always')
    file = st.file_uploader("Upload a datapack", type=["zip"])
    if file is not None:
        biome_folders = check_for_biome_folders(file)
        if len(biome_folders) > 0:
            st.info("The following biome folders were found:")
            for folder in biome_folders:
                st.write(folder)
            st.caption("Parsed in " + str(int((end - start)*1000)) + "ms")
            create_json_file(file)
            with open("en_us.json", "r") as infile:
                json_data = json.load(infile)
            st.download_button("Download Lang JSON", json.dumps(json_data, indent=2), file_name="en_us.json")
        else:
            st.error("No biome folders were found.")


if __name__ == "__main__":
    main()
