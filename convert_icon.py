from PIL import Image
img = Image.open(r'C:\Users\okoth\.gemini\antigravity\brain\15862444-89f4-4418-abc2-a2d3a4f35c0e\media_yantra_logo_1783616501310.png')
img.convert('RGBA').save(r'o:\media yantra\assets\icon.ico', format='ICO')
