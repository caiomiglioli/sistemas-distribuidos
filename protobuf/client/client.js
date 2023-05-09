const net = require('net');
const protos = require('google-protobuf');
const prompt = require('prompt-sync')();
const { Command, MoviesList } = require('./movies_pb');

const {PromiseSocket, TimeoutError} = require("promise-socket")

const client = new net.Socket();
const promiseSocket = new PromiseSocket(client)

client.connect(7777, 'localhost', function (){
  console.log('Connect');

  // firstOutput();
  // getInputs();
  handleListByActor('John McCann')

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

const getInputs = () => {
  while (true) {
    const input = prompt('> ');
    [cmd, arg] = input.split(' ')

    if (cmd === 'ListByActor'){
      handleListByActor(arg)
    }

    // if (options.includes(input.trim())) {
    //   let message = setMessageType(input.trim());
    //   console.log(message);

    // }
    // else if(input === 'close'){
    //   client.destroy();
    //   break;
    // }  
  }
}

const  handleListByActor = async (arg) =>{
  const cmd = new Command();
  cmd.setCmd("ListByActor")
  cmd.addArgs(arg)
  const sCmd = cmd.serializeBinary();

  client.write(toBytesInt32(sCmd.length))
  client.write(sCmd)

  //receber 4 bytes pra inteiro
  //receber o resto do pacote
  const dataSize = await promiseSocket.read(4)
  const data = await promiseSocket.read(bytesToNum(dataSize))
  

  const mList = MoviesList.deserializeBinary(data)

  console.log(mList.getMoviesList())
}

function toBytesInt32(num) {
  arr = new ArrayBuffer(4); // an Int32 takes 4 bytes
  view = new DataView(arr);
  view.setUint32(0, num, false); // byteOffset = 0; litteEndian = false
  return new Uint8Array(arr);
}

function bytesToNum(bytes){
  const buffer = Buffer.from(bytes); // buffer com 4 bytes
  return buffer.readUInt32BE();
}