def generate_audio_options(base_options, codec="mp3", quality="320", embed_thumb=True, embed_metadata=True):
    opts = base_options.copy()
    
    opts['format'] = 'bestaudio/best'
    opts['postprocessors'] = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': codec.lower(),
        'preferredquality': quality.replace(" kbps", ""),
    }]
    
    if embed_thumb:
        opts['writethumbnail'] = True
        opts['postprocessors'].append({'key': 'EmbedThumbnail'})
        
    if embed_metadata:
        opts['postprocessors'].append({'key': 'FFmpegMetadata'})
        
    return opts
