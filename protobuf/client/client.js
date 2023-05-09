const net = require('net');
// const protos = require('googele-protobuf');
// const protobuf = require('protobuf');
const prompt = require('prompt-sync')();
// const { Movie } = require('./movies_pb');

const options = ['create', 'read', 'update', 'delete', 'list']

const CREATE = 1;
const UPDATE = 2;
const DELETE = 3;
const LIST = 4;

const client = new net.Socket();

client.connect(7777, 'localhost', function (){
  console.log('Connect');

  firstOutput();
  getInputs();
})

const firstOutput = () => {
  console.log('Esse cliente permite as seguintes operações (digite seu nome indicado, não o número): ');
  console.log('1. Create');
  console.log('2. Update');
  console.log('3. Delete');
  console.log('4. List');
  console.log('5. Close');
  console.log('Qual operação deseja fazer?: ');
}

const getInputs = () => {
  while (true) {
    const input = prompt('> ');
    if (options.includes(input.trim())) {
      let message = setMessageType(input.trim());
      console.log(message);

    }
    else if(input === 'close'){
      client.destroy();
      break;
    }  
  }
}

const setMessageType = (input) =>{
  let message = 0;

  switch (input) {
    case 'create':
      console.log('caso1');
      message = CREATE;
      break;

    case 'update':
      message = UPDATE;
      break;

    case 'delete':
      message = DELETE;
      break;

    case 'list':
      message = LIST;
      break;

    default:
      message = undefined;
      break;
  }

  return message;
}

// const toBytes = (num) => {
//   return Buffer.from(num.toString(16).padStart(2, '0'), 'hex');
// }