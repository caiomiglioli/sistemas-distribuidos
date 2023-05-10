const net = require('net');
const protos = require('google-protobuf');
const prompt = require('prompt-sync')();
const { Command, MoviesList, Movie } = require('./movies_pb');

const { PromiseSocket, TimeoutError } = require("promise-socket")

const client = new net.Socket();
const promiseSocket = new PromiseSocket(client)


client.connect(7778, 'localhost', function () {
  console.log('Connect');

  // firstOutput();
  getInputs();


})

// const firstOutput = () => {
//   console.log('Esse cliente permite as seguintes operações (digite seu nome indicado, não o número): ');
//   console.log('1. Create');
//   console.log('2. Update');
//   console.log('3. Delete');
//   console.log('4. List');
//   console.log('5. Close');
//   console.log('Qual operação deseja fazer?: ');
// }

const getInputs = async () => {
  while (true) {
    const input = prompt('> ');
    [cmd, arg] = input.split(' ')

    if (cmd === 'ListByActor') {
      await handleListByActor(arg)
    } else if (cmd === 'ListByGenre') {
      await handleListByGenre(arg)
    } else if (cmd === 'Read') {
      await handleRead(arg)
    } else if (cmd === 'Create') {
      await handleCreate(arg)
    } else if (cmd === 'Update') {
      await handleUpdate(arg)
    } else if (cmd === 'Delete') {
      await handleDelete(arg)
    }
    else if (input === 'close') {
      client.destroy();
      break;
    } else {
      console.log('Comando inexistente.')
    }
  }
}

const handleListByActor = async (arg) => {
  sendCommand("ListByActor", arg)
  const data = await receiveData()
  const mList = MoviesList.deserializeBinary(data)
  mList.getMoviesList().forEach((e)=>{
    printMovie(e.toObject())
  })
}

const handleListByGenre = async (arg) => {
  sendCommand("ListByGenre", arg)
  const data = await receiveData()
  const mList = MoviesList.deserializeBinary(data)
  mList.getMoviesList().forEach((e)=>{
    printMovie(e.toObject())
  })
}


const handleRead = async (arg) => {
  sendCommand("Read", arg)
  data = await receiveData()
  const movie = Movie.deserializeBinary(data)
  printMovie(movie.toObject())
}

const handleCreate = async () => {
  sendCommand("Create", "N/A")

  const defaultMovie = {
      'plot': 'N/A',
      'genresList': ['N/A'],
      'runtime': -1,
      'rated': 'N/A',
      'castList': [],
      'poster': 'N/A',
      'title': 'N/A',
      'fullplot': "N/A",
      'year': -1,
      'type': 'N/A',
      'writersList': [],
      'countriesList': [],
      'languagesList': [],
      'directorsList': [],
  }
  
  const m = editMovieToProtobuf(defaultMovie);
  const mProto = m.serializeBinary()
  client.write(toBytesInt32(mProto.length));
  client.write(mProto);

  data = await receiveData()
  const res = Command.deserializeBinary(data)
  if (res.getCmd() === "Success") {
    console.log("Sucesso na criação do filme: ", m.getTitle())
  } else {
    console.log("Falha na criação do filme")
  }
}

const handleUpdate = async (arg) => {
  //enviou o comando
  sendCommand("Update", arg)

  //recebe protobuf do movie
  data = await receiveData()
  const movie = Movie.deserializeBinary(data)
  const mAux = movie.toObject()

  //edita e devolve pro servidor
  const m = editMovieToProtobuf(mAux);
  const mProto = m.serializeBinary()
  client.write(toBytesInt32(mProto.length));
  client.write(mProto);

  //recebe a confirmação
  data = await receiveData()
  const res = Command.deserializeBinary(data)
  if (res.getCmd() === "Success") {
    console.log("Sucesso na atualização do filme: ", m.getTitle())
  } else {
    console.log("Falha na atualização do filme")
  }
}

const handleDelete = async (arg) => {
  sendCommand("Delete", arg)
  data = await receiveData()
  const res = Command.deserializeBinary(data)
  if (res.getCmd() === "Success") {
    console.log("Sucesso na exclusão do filme com o id: ", arg)
  } else {
    console.log("Falha na exclusão do filme com id: ", arg)
  }
}

const sendCommand = (command, arg) => {
  const cmd = new Command();
  cmd.setCmd(command)
  cmd.addArgs(arg)
  const sCmd = cmd.serializeBinary();
  client.write(toBytesInt32(sCmd.length))
  client.write(sCmd)
}

const receiveData = async () => {
  const dataSize = await promiseSocket.read(4)
  const data = await promiseSocket.read(bytesToNum(dataSize))
  return data
}

const printMovie = (movie) =>{
  console.log(movie)
}


function toBytesInt32(num) {
  arr = new ArrayBuffer(4); // an Int32 takes 4 bytes
  view = new DataView(arr);
  view.setUint32(0, num, false); // byteOffset = 0; litteEndian = false
  return new Uint8Array(arr);
}

function bytesToNum(bytes) {
  const buffer = Buffer.from(bytes); // buffer com 4 bytes
  return buffer.readUInt32BE();
}


const editMovieToProtobuf = (movie) => {
  const m = new Movie();
  m.id = 'NEW';
  var input = null;

  console.log('==== 1. CAMPO PLOT\nValor atual: ', movie.plot)
  input = prompt('Novo valor > ');
  if (input) m.setPlot(input)
    else m.setPlot(movie.plot)

  console.log('==== 2. CAMPO GENRES\nValor atual: ', movie.genresList)
  input = prompt('Novo valor > ');
  if (input) input.split(' ').forEach(i => m.addGenres(i));
    else movie.genresList.forEach(i => m.addGenres(i));

  console.log('==== 3. CAMPO RUNTIME\nValor atual: ', movie.runtime)
  input = prompt('Novo valor > ');
  if (input) m.setRuntime(input)
    else m.setRuntime(movie.runtime)

  console.log('==== 4. CAMPO RATED\nValor atual: ', movie.rated)
   input = prompt('Novo valor > ');
  if (input) m.setRated(input)
    else m.setRated(movie.rated)

  console.log('==== 5. CAMPO CAST\nValor atual: ', movie.castList)
  input = prompt('Novo valor > ');
  if (input) input.split(' ').forEach(i => m.addCast(i));
    else movie.castList.forEach(i => m.addCast(i));

  console.log('==== 6. CAMPO POSTER\nValor atual: ', movie.poster)
  input = prompt('Novo valor > ');
  if (input) m.setPoster(input)
    else m.setPoster(movie.poster)

  console.log('==== 7. CAMPO TITLE\nValor atual: ', movie.title)
  input = prompt('Novo valor > ');
  if (input) m.setTitle(input)
    else m.setTitle(movie.title)

  console.log('==== 8. CAMPO FULLPLOT\nValor atual: ', movie.fullplot)
  input = prompt('Novo valor > ');
  if (input) m.setFullplot(input)
    else m.setFullplot(movie.fullplot)

  console.log('==== 9. CAMPO YEAR\nValor atual: ', movie.year)
  input = prompt('Novo valor > ');
  if (input) m.setYear(input)
    else m.setYear(movie.year)

  console.log('==== 10. CAMPO TYPE\nValor atual: ', movie.type)
  input = prompt('Novo valor > ');
  if (input) m.setType(input)
    else m.setType(movie.type)

  console.log('==== 11. CAMPO WRITERS\nValor atual: ', movie.writersList)
  input = prompt('Novo valor > ');
  if (input) {
    input.split(' ').forEach(i => m.addWriters(i));
  } else movie.writersList.forEach(i => m.addWriters(i));
 
  console.log('==== 12. CAMPO COUNTRIES\nValor atual: ', movie.countriesList)
  input = prompt('Novo valor > ');
  if (input) {
    input.split(' ').forEach(i => m.addCountries(i));
  } else movie.countriesList.forEach(i => m.addCountries(i));

  console.log('==== 13. CAMPO LANGUAGES\nValor atual: ', movie.languagesList)
  input = prompt('Novo valor > ');
  if (input) {
    input.split(' ').forEach(i => m.addLanguages(i));
  } else movie.languagesList.forEach(i => m.addLanguages(i));

  console.log('==== 14. CAMPO DIRECTORS\nValor atual: ', movie.directorsList)
  input = prompt('Novo valor > ');
  if (input) {
    input.split(' ').forEach(i => m.addDirectors(i));
  } else movie.directorsList.forEach(i => m.addDirectors(i));

  return m;
}

