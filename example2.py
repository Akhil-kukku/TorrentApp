import libtorrent as lt
import time
import os
from tqdm import tqdm

def download_selected_files(torrent_file, download_path, selected_files):
    # Create a session and listen on port 6881 (default BitTorrent port)
    ses = lt.session()
    ses.listen_on(6881, 6891)

    # Load the torrent file
    info = lt.torrent_info(torrent_file)

    # Print all files in the torrent
    print("Files in the torrent:")
    for idx, f in enumerate(info.files()):
        print(f"{idx}: {f.path} ({f.size / 1024:.2f} KB)")

    # Set the file priorities (0 = do not download, 1 = download)
    file_priorities = [0] * len(info.files())  # Default to 0 (do not download)
    for idx in selected_files:
        file_priorities[idx] = 1  # Set priority for selected files to 1 (download)

    params = {
        'save_path': download_path,  # Where the files will be saved
        'ti': info,  # Torrent info object
        'file_priorities': file_priorities  # Apply file priorities
    }

    # Add the torrent to the session
    handle = ses.add_torrent(params)
    print(f"Starting download of selected files in {handle.name()}...")

    # Get the total size of selected files
    # Use a list comprehension to get the file sizes and then sum them
    total_size = sum([f.size for i, f in enumerate(info.files()) if i in selected_files])

    # Initialize tqdm progress bar
    pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")

    # Monitor the download progress
    while not handle.is_seed():
        s = handle.status()

        # Update the progress bar with the number of bytes downloaded
        pbar.update(int(s.total_done - pbar.n))

        # Display additional information about the download status
        print(f"\rProgress: {s.progress * 100:.2f}% "
              f"Download speed: {s.download_rate / 1000:.2f} kB/s "
              f"Peers: {s.num_peers}", end='')
        time.sleep(1)

    # Close the progress bar after the download is complete
    pbar.close()

    print(f"\nDownload complete: {handle.name()}")

if __name__ == '__main__':
    torrent_file = '/content/ColdplayASkyFullOfStarsOfficialVideo_201709_archive.torrent'  # Example: 'myfile.torrent'
    download_path = '/content'  # Example: '/downloads/'

    # Ensure the download directory exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Load torrent info to list the files
    info = lt.torrent_info(torrent_file)
    print("Files in the torrent:")
    for idx, f in enumerate(info.files()):
        print(f"{idx}: {f.path} ({f.size / 1024:.2f} KB)")

    # Ask the user to input file indices
    selected_files_input = input("Enter file indices to download (comma-separated): ")
    selected_files = list(map(int, selected_files_input.split(',')))

    # Download the selected files
    download_selected_files(torrent_file, download_path, selected_files)
