# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import movies_pb2 as movies__pb2


class MoviesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListByGenre = channel.unary_stream(
                '/moviespackage.Movies/ListByGenre',
                request_serializer=movies__pb2.Msg.SerializeToString,
                response_deserializer=movies__pb2.Movie.FromString,
                )
        self.ListByActor = channel.unary_stream(
                '/moviespackage.Movies/ListByActor',
                request_serializer=movies__pb2.Msg.SerializeToString,
                response_deserializer=movies__pb2.Movie.FromString,
                )
        self.Create = channel.unary_unary(
                '/moviespackage.Movies/Create',
                request_serializer=movies__pb2.Movie.SerializeToString,
                response_deserializer=movies__pb2.Msg.FromString,
                )
        self.Read = channel.unary_unary(
                '/moviespackage.Movies/Read',
                request_serializer=movies__pb2.Msg.SerializeToString,
                response_deserializer=movies__pb2.Movie.FromString,
                )
        self.Delete = channel.unary_unary(
                '/moviespackage.Movies/Delete',
                request_serializer=movies__pb2.Msg.SerializeToString,
                response_deserializer=movies__pb2.Msg.FromString,
                )


class MoviesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListByGenre(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListByActor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """rpc Update(????) returns (Msg) {};
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MoviesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListByGenre': grpc.unary_stream_rpc_method_handler(
                    servicer.ListByGenre,
                    request_deserializer=movies__pb2.Msg.FromString,
                    response_serializer=movies__pb2.Movie.SerializeToString,
            ),
            'ListByActor': grpc.unary_stream_rpc_method_handler(
                    servicer.ListByActor,
                    request_deserializer=movies__pb2.Msg.FromString,
                    response_serializer=movies__pb2.Movie.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=movies__pb2.Movie.FromString,
                    response_serializer=movies__pb2.Msg.SerializeToString,
            ),
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=movies__pb2.Msg.FromString,
                    response_serializer=movies__pb2.Movie.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=movies__pb2.Msg.FromString,
                    response_serializer=movies__pb2.Msg.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'moviespackage.Movies', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Movies(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListByGenre(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/moviespackage.Movies/ListByGenre',
            movies__pb2.Msg.SerializeToString,
            movies__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListByActor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/moviespackage.Movies/ListByActor',
            movies__pb2.Msg.SerializeToString,
            movies__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/moviespackage.Movies/Create',
            movies__pb2.Movie.SerializeToString,
            movies__pb2.Msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/moviespackage.Movies/Read',
            movies__pb2.Msg.SerializeToString,
            movies__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/moviespackage.Movies/Delete',
            movies__pb2.Msg.SerializeToString,
            movies__pb2.Msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)