const grpc = require('@grpc/grpc-js')
var protoLoader = require('@grpc/proto-loader');

// //grpc promise => https://github.com/carlessistare/grpc-promise#readme
// const grpc_promise = require('grpc-promise');
// grpc_promise.promisifyAll(stub); //transforma tudo em promise pra usar async await

// ================= CHAMADAS =======================

async function handleRead(stub, Msg){
    await new Promise((resolve, reject) => {
        // **** comandos do grpc sempre dentro da promise **** 

        //chama funcao read do stub, com Msg de parametro e callback
        stub.Read(Msg, (error, Movie) => {
            if (error) reject(error);
            
            //Tratamento da funcao
            console.log('success =>>>', Movie)
            
            //dentro da promise, resolve() = return
            resolve()
        })
    })
}

// ~~~~~ ListByActor (stream do servidor) ~~~~
async function handleListByActor(stub, Msg){    
    await new Promise((resolve, reject) => {
        //chama funcao read do stub, com Msg de parametro
        var call = stub.ListByActor(Msg);       
        
        //fica recebendo movie em stream
        call.on('data', (Movie) => {            
            console.log('\n==================== Movie ====================\n')
            console.log(Movie);
        });
        
        //é chamado quando o servidor termina de mandar os movie
        call.on('end', () => {                  
            console.log('*** end ***')
            resolve()
        });
        
        //em caso de erro
        call.on('error', (e) => {
            reject(e)
        });
    })
};


// ================= CLIENT ORCHESTRA =======================

const main = async () => {
    //stub = client
    var packageDefinition = protoLoader.loadSync('../protos/movies.proto');
    var moviespackage = grpc.loadPackageDefinition(packageDefinition).moviespackage
    var stub = new moviespackage.Movies('localhost:7777', grpc.credentials.createInsecure());

    //Read
    var Msg = {'message': 'Your Highness'} //criar um objeto com as mesmas chaves do movies.proto
    await handleRead(stub, Msg)
    
    //ListByActor
    Msg = {'message': 'James'}
    await handleListByActor(stub, Msg)


    console.log('ISSO TEM QUE VIR DEPOIS DE TUDO')
}

main()
