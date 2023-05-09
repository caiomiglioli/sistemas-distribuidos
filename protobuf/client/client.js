const net = require('net');
// const protos = require('googele-protobuf');
// const protobuf = require('protobuf');
const prompt = require('prompt-sync')();
// const { Movie } = require('./movies_pb');

const options = ['create', 'read', 'update', 'delete', 'list']

const CREATE = 1;
const READ = 2;
const UPDATE = 3;
const DELETE = 4;
const LIST = 5;

const client = new net.Socket();

client.connect(7777, 'localhost', function (){
  console.log('Connect');

  firstOutput();
  getInputs();
})

const firstOutput = () => {
  console.log('Esse cliente permite as seguintes operações (digite seu nome indicado, não o número): ');
  console.log('1. Create');
  console.log('2. Read');
  console.log('3. Update');
  console.log('4. Delete');
  console.log('5. List');
  console.log('6. Close');
  console.log('Qual operação deseja fazer?: ');
}

const getInputs = () => {
  while (true) {
    const input = prompt('> ');
    if (options.includes(input.trim())) {
      var message = setMessageType(input.trim());


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
      message += toBytes(CREATE);
      break;

    case 'read':
      message += toBytes(READ);
      break;

    case 'update':
      message += toBytes(UPDATE);
      break;

    case 'delete':
      message += toBytes(DELETE);
      break;

    case 'list':
      message += toBytes(LIST);
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