from pytube import YouTube
import openai
import os

# Configure sua chave da OpenAI
openai.api_key = "sk-..."

def solicitar_url():
    print("\n" + "=" * 50)
    print(" RESUMO AUTOMÁTICO DE VÍDEOS DO YOUTUBE")
    print("=" * 50 + "\n")
    url = input("Por favor, insira a URL do vídeo do YouTube que deseja resumir:\nURL: ").strip()
    while not ("youtube.com" in url or "youtu.be" in url):
        print("URL inválida! Tente novamente.")
        url = input("URL: ").strip()
    return url

def baixar_audio(url, filename="audio.mp4"):
    try:
        print("Baixando áudio do vídeo...")
        yt = YouTube(url)
        print(f"Vídeo encontrado: {yt.title}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename=filename)
        print(f"Áudio salvo como {filename}")
        return filename
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")
        return None

def transcrever_audio(filename):
    try:
        print("Transcrevendo áudio...")
        with open(filename, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print("Transcrição concluída!")
        return transcript["text"]
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return None

def gerar_resumo(transcricao):
    try:
        print("Gerando resumo...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Você é um assistente que resume vídeos detalhadamente. "
                    "Gere um resumo completo com tópicos principais, pontos-chave e conclusões. "
                    "Use marcações Markdown para organização."
                )},
                {"role": "user", "content": f"Resuma detalhadamente o seguinte conteúdo:\n\n{transcricao}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return None

def main():
    url = solicitar_url()
    audio_file = baixar_audio(url)
    if not audio_file:
        return
    transcricao = transcrever_audio(audio_file)
    if not transcricao:
        return
    resumo = gerar_resumo(transcricao)
    if not resumo:
        return
    with open("Resumo.md", "w", encoding="utf-8") as f:
        f.write(resumo)
    print("Resumo salvo em Resumo.md")
    os.remove(audio_file)
    print("Processo concluído!")

if __name__ == "__main__":
    main()
