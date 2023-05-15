from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Movie(_message.Message):
    __slots__ = ["cast", "countries", "directors", "fullplot", "genres", "id", "languages", "plot", "poster", "rated", "runtime", "title", "type", "writers", "year"]
    CAST_FIELD_NUMBER: _ClassVar[int]
    COUNTRIES_FIELD_NUMBER: _ClassVar[int]
    DIRECTORS_FIELD_NUMBER: _ClassVar[int]
    FULLPLOT_FIELD_NUMBER: _ClassVar[int]
    GENRES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    PLOT_FIELD_NUMBER: _ClassVar[int]
    POSTER_FIELD_NUMBER: _ClassVar[int]
    RATED_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WRITERS_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    cast: _containers.RepeatedScalarFieldContainer[str]
    countries: _containers.RepeatedScalarFieldContainer[str]
    directors: _containers.RepeatedScalarFieldContainer[str]
    fullplot: str
    genres: _containers.RepeatedScalarFieldContainer[str]
    id: str
    languages: _containers.RepeatedScalarFieldContainer[str]
    plot: str
    poster: str
    rated: str
    runtime: int
    title: str
    type: str
    writers: _containers.RepeatedScalarFieldContainer[str]
    year: int
    def __init__(self, id: _Optional[str] = ..., plot: _Optional[str] = ..., genres: _Optional[_Iterable[str]] = ..., runtime: _Optional[int] = ..., rated: _Optional[str] = ..., cast: _Optional[_Iterable[str]] = ..., poster: _Optional[str] = ..., title: _Optional[str] = ..., fullplot: _Optional[str] = ..., year: _Optional[int] = ..., type: _Optional[str] = ..., writers: _Optional[_Iterable[str]] = ..., countries: _Optional[_Iterable[str]] = ..., languages: _Optional[_Iterable[str]] = ..., directors: _Optional[_Iterable[str]] = ...) -> None: ...

class MoviesList(_message.Message):
    __slots__ = ["movies"]
    MOVIES_FIELD_NUMBER: _ClassVar[int]
    movies: _containers.RepeatedCompositeFieldContainer[Movie]
    def __init__(self, movies: _Optional[_Iterable[_Union[Movie, _Mapping]]] = ...) -> None: ...

class Msg(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
