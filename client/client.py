from modules.fetch import Fetch

def main():
    apiUrl = 'http://127.0.0.1:3000'
    # Send video
    with open('./storage/video.mp4', 'rb') as arquivo:
        blob = arquivo.read()
        video = {
            "title": 'Nuevo Video',
            "blob": blob,
            "size": len(blob)
        }
        response = Fetch.post(f'{apiUrl}/video', video)
    
    with open('./storage/video2.mp4', 'rb') as arquivo:
        blob = arquivo.read()
        video = {
            "title": 'Nuevo Video 2',
            "blob": blob,
            "size": len(blob)
        }
        Fetch.post(f'{apiUrl}/video', video)
    
    # Get video by ID
    print("GET")
    video_id = 1
    video_obtido = Fetch.post(f'{apiUrl}/video/id', {
        "id": video_id
    })
    print(f"Vídeo obtido por ID {video_id}: {video_obtido['title']}")

    video_a_remover = 5
    video_obtido = Fetch.delete(f'{apiUrl}/video', {
        "id": video_a_remover
    })
    if(video_obtido != None):
        print(f"Vídeo obtido por ID {video_id}: {video_obtido['title']}")

    todos_os_videos = Fetch.get(f'{apiUrl}/videos')

    print("Todos os vídeos no banco de dados:")
    for video in todos_os_videos:
        print(video['id'], video['title'])


if __name__ == "__main__":
    main()