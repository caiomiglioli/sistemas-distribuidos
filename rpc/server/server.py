#utils
from concurrent import futures

#rpc protobuf
import grpc
import movies_pb2
import movies_pb2_grpc
from google.protobuf.json_format import MessageToJson

#db
from db import MongoDBClient

class MoviesServicer(movies_pb2_grpc.MoviesServicer):
    def __init__(self):
        self.db = MongoDBClient()

    def ListByGenre(self, request, context):
        movies = self.db.listByGenre(request.message)
        for movie in movies:
            yield movieToProtobuf(movie)

    def ListByActor(self, request, context):
        movies = self.db.listByActor(request.message)
        for movie in movies:
            yield movieToProtobuf(movie)
    
    def Create(self, request, context):
        print(request)
        result = self.db.create(MessageToJson(request))
        return movies_pb2.Msg(
            message = 'Success' if result else 'Failure'
        )

    def Read(self, request, context):
        movie = self.db.getByTitle(request.message)
        if not movie:
            movie = {'_id': 'Não encontrado'}
        return movieToProtobuf(movie)

    def Update(self, request_iterator, context):
        movieId = None
        for request in request_iterator:
            if request.order == 0:
                movieId = request.arg
                movieToEdit = self.db.getById(movieId)
                yield movies_pb2.Update_(
                    order = 1,
                    movie = movieToProtobuf(movieToEdit)
                )

            elif request.order == 2:
                result = self.db.update(movieId, MessageToJson(request.movie)) if movieId else None
                yield movies_pb2.Update_(
                    order = 3,
                    arg = 'Success' if result else 'Failure'
                )
                break

            else:
                yield movies_pb2.Update_(order = 3, arg = 'Failure')
                break
        #end for
    #end update

    def Delete(self, request, context):
        result = self.db.delete(request.message)
        return movies_pb2.Msg(
            message = 'Success' if result else 'Failure'
        )
    #end delete
#end class

def movieToProtobuf(movie):
    """
    Cria e retorna uma instância de protobuf Movie a
    partir de um dicionário (movie).
    """
    m = movies_pb2.Movie()
    m.id = str(movie['_id'])
    m.title = movie['title'] if movie.get('title') else "N/A"
    m.poster = movie['poster'] if movie.get('poster') else "N/A"
    m.rated = movie['rated'] if movie.get('rated') else "N/A"
    m.type = movie['type'] if movie.get('type') else "N/A"
    m.plot = movie['plot'] if movie.get('plot') else "N/A"
    m.fullplot = movie['fullplot'] if movie.get('fullplot') else "N/A"
    m.runtime = movie['runtime'] if movie.get('runtime') else -1
    m.year = int(str(movie.get('year')).split('è')[0]) if movie.get('year') else -1
    if movie.get('cast'): m.cast.extend(movie['cast'])
    if movie.get('genres'): m.genres.extend(movie['genres'])
    if movie.get('countries'): m.countries.extend(movie['countries'])
    if movie.get('directors'): m.directors.extend(movie['directors'])
    if movie.get('writers'): m.writers.extend(movie['writers'])
    if movie.get('languages'): m.writers.extend(movie['languages'])
    return m #.SerializeToString()


# ~~~~~~~~~~~~~~~~~~~~~~~~~ SERVER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movies_pb2_grpc.add_MoviesServicer_to_server(MoviesServicer(), server)
    server.add_insecure_port('[::]:7777')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__': 
    serve()