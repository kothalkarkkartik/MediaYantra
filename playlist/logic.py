def generate_playlist_options(base_options, selection_type="all", range_str="", resolution="Best Quality"):
    """
    Generates yt-dlp options based on the user's playlist selection.
    selection_type: 'all', 'range', 'random', 'last'
    """
    opts = base_options.copy()
    
    if selection_type == "range" and range_str:
        # User input could be "1-25"
        opts['playlist_items'] = range_str
    elif selection_type == "last" and range_str:
        # Use negative indices? yt-dlp supports playlist end. We'll simplify to -range
        # E.g. range_str="10" meaning last 10
        opts['playlistend'] = -1
        opts['playliststart'] = -int(range_str)
    elif selection_type == "random":
        opts['playlistrandom'] = True
        
    opts['extract_flat'] = False
    
    # Format
    if resolution == "Audio Only":
        opts['format'] = 'bestaudio/best'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif resolution != "Best Quality":
        height = resolution.replace("p", "").replace("K", "000") # simplistic conversion
        opts['format'] = f'bestvideo[height<={height}]+bestaudio/best'
    else:
        opts['format'] = 'bestvideo+bestaudio/best'
        
    return opts
