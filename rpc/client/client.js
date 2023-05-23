/*
Este código implementa a parte cliente de um programa cliente/servidor
de gerenciamento de uma base de dados de filmes, onde a comunicação
ocorre via RPC e Protobuf. É utilizado o gRPC como framework.

Autores:
  - Caio Miglioli @caiomiglioli
  - Ryan Lazaretti @ryanramos01

Data de Criação: 19 de Maio de 2023
Ultima alteração: 23 de Maio de 2023
*/

const grpc = require('@grpc/grpc-js')
var protoLoader = require('@grpc/proto-loader');
const prompt = require('prompt-sync')();

// //grpc promise => https://github.com/carlessistare/grpc-promise#readme
// const grpc_promise = require('grpc-promise');
// grpc_promise.promisifyAll(stub); //transforma tudo em promise pra usar async await

// ================= CHAMADAS =======================

async function handleRead(stub, movieName){
    // É criado uma promise para que o cliente funcione de maneira sincrona
    // A promise é retornada somente após o callback do stub, assim travando
    // o cliente nessa função até que tudo se resolva.
    await new Promise((resolve, reject) => {
        // **** comandos do grpc sempre dentro da promise **** 

        //chama funcao read do stub, com Msg de parametro e callback
        stub.Read({'message' : movieName}, (error, Movie) => {
            if (error) reject(error);
            
            //Tratamento da funcao
            console.log(Movie)
            
            //dentro da promise, resolve() = return
            resolve()
        })
    })
}

async function handleDelete(stub, movieId){
    await new Promise((resolve, reject) => {
        // **** comandos do grpc sempre dentro da promise **** 

        //chama funcao delete do stub, com Msg de parametro e callback
        stub.Delete({'message' : movieId}, (error, message) => {
            if (error) reject(error);
            
            //Tratamento da funcao
            console.log(message.message)
            
            //dentro da promise, resolve() = return
            resolve()
        })
    })
}


async function handleCreate(stub){
    const defaultMovie = {
        'plot': 'N/A',
        'genres': ['N/A'],
        'runtime': -1,
        'rated': 'N/A',
        'cast': [],
        'poster': 'N/A',
        'title': 'N/A',
        'fullplot': "N/A",
        'year': -1,
        'type': 'N/A',
        'writers': [],
        'countries': [],
        'languages': [],
        'directors': [],
    }
    
    const movie = editMovie(defaultMovie)

    await new Promise((resolve, reject) => {
        // **** comandos do grpc sempre dentro da promise **** 

        //chama funcao delete do stub, com Msg de parametro e callback
        stub.Create(movie, (error, message) => {
            if (error) reject(error);
            
            //Tratamento da funcao
            console.log(message.message)
            
            //dentro da promise, resolve() = return
            resolve()
        })
    })
}

// ~~~~~ ListByActor (stream do servidor) ~~~~
async function handleListByActor(stub, nameActor){    
    await new Promise((resolve, reject) => {
        //chama funcao read do stub, com Msg de parametro
        var call = stub.ListByActor({'message' : nameActor});       
        
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

// ~~~~~ ListByGenre (stream do servidor) ~~~~
async function handleListByGenre(stub, nameGenre){    
    await new Promise((resolve, reject) => {
        //chama funcao read do stub, com Msg de parametro
        var call = stub.ListByGenre({'message' : nameGenre});       
        
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

// ~~~~~ Update (stream duplex) ~~~~
async function handleUpdate(stub, movieId){    
    await new Promise((resolve, reject) => {
        // ORDERS
        // 0 -> cliente pede filme pro servidor
        // 1 -> servidor manda filme pro cliente
        // 2 -> cliente manda filme editado pro servidor
        // 3 -> servidor retorna com o resultado do update

        //chama funcao read do stub
        var call = stub.Update();

        //envia o id do filme
        call.write({'order': 0, 'arg': movieId})

        //fica recebendo em stream
        call.on('data', (upd) => {
            if (upd.order === 1){
                console.log(`============= Editando  "${upd.movie.title}" =============`)
                const movie = editMovie(upd.movie)
                call.write({'order': 2, 'movie': movie});
            } else {
                if (upd.order === 3) console.log(upd.arg)
                else console.log('Failure')
                call.end();
            }
        });
        
        //é chamado quando o servidor termina de mandar os movie
        call.on('end', () => {
            resolve()
        });
        
        //em caso de erro
        call.on('error', (e) => {
            reject(e)
        });
    })
}


// ================= HELPERS =======================
//função auxiliar para criação e update de um movie passado.
const editMovie = (movie) => {
    var input = null;
  
    console.log('==== 1. CAMPO PLOT\nValor atual: ', movie.plot)
    input = prompt('Novo valor > ');
    if (input) movie.plot = input

    console.log('==== 2. CAMPO GENRES\nValor atual: ', movie.genres)
    input = prompt('Novo valor > ');
    if (input) movie.genres = input.split(' ')
  
    console.log('==== 3. CAMPO RUNTIME\nValor atual: ', movie.runtime)
    input = prompt('Novo valor > ');
    if (input) movie.runtime = input

    console.log('==== 4. CAMPO RATED\nValor atual: ', movie.rated)
     input = prompt('Novo valor > ');
     if (input) movie.rated = input
  
    console.log('==== 5. CAMPO CAST\nValor atual: ', movie.cast)
    input = prompt('Novo valor > ');
    if (input) movie.cast = input.split(' ')
  
    console.log('==== 6. CAMPO POSTER\nValor atual: ', movie.poster)
    input = prompt('Novo valor > ');
    if (input) movie.poster = input

    console.log('==== 7. CAMPO TITLE\nValor atual: ', movie.title)
    input = prompt('Novo valor > ');
    if (input) movie.title = input
  
    console.log('==== 8. CAMPO FULLPLOT\nValor atual: ', movie.fullplot)
    input = prompt('Novo valor > ');
    if (input) movie.fullplot = input

    console.log('==== 9. CAMPO YEAR\nValor atual: ', movie.year)
    input = prompt('Novo valor > ');
    if (input) movie.year = input
  
    console.log('==== 10. CAMPO TYPE\nValor atual: ', movie.type)
    input = prompt('Novo valor > ');
    if (input) movie.type = input
  
    console.log('==== 11. CAMPO WRITERS\nValor atual: ', movie.writers)
    input = prompt('Novo valor > ');
    if (input) movie.cast = input.split(' ')
   
    console.log('==== 12. CAMPO COUNTRIES\nValor atual: ', movie.countries)
    input = prompt('Novo valor > ');
    if (input) movie.countries = input.split(' ')
  
    console.log('==== 13. CAMPO LANGUAGES\nValor atual: ', movie.languages)
    input = prompt('Novo valor > ');
    if (input) movie.languages = input.split(' ')
  
    console.log('==== 14. CAMPO DIRECTORS\nValor atual: ', movie.directors)
    input = prompt('Novo valor > ');
    if (input) movie.languages = input.split(' ')

    return movie
  }

//função que valida se o argumento digitado é válido
const thereIsArgument = (arg) =>{
    const size = arg.length
    if (size < 1) return false
    return true
  }
//função que valida se o comando digitado é valido
const validCommand = (cmd) =>{
    if (cmd != 'ListByActor' && cmd != 'ListByGenre' && cmd != 'Create' && cmd != 'Read' && cmd != 'Update' && cmd != 'Delete' && cmd != 'Close')
        return false
    return true
}

//outputs iniciais
const initialOutputs = () =>{
    console.log('=================Cliente RPC=================')
    console.log('Lista de comandos:')
    console.log('ListByActor (arg)')
    console.log('ListByGenre (arg)')
    console.log('Create')
    console.log('Read (arg)')
    console.log('Update (arg)')
    console.log('Delete (arg)')
    console.log('Close')
    console.log('==============================================')
}

// ================= CLIENT ORCHESTRA =======================

const getInputs = async (stub) => {
    initialOutputs()
    while (true) {
        const input = prompt('> ');
        [cmd, arg] = input.split(' ')
        
        if (validCommand(cmd)){
            if (cmd === 'Create') await handleCreate(stub)
            if (thereIsArgument(arg)){
                if (cmd === 'ListByActor') {
                    await handleListByActor(stub, arg)
                } else if (cmd === 'ListByGenre') {
                    await handleListByGenre(stub, arg)
                } else if (cmd === 'Read') {
                    await handleRead(stub, arg)
                } else if (cmd === 'Update') {
                    await handleUpdate(stub, arg)
                } else if (cmd === 'Delete') {
                    await handleDelete(stub, arg)
                }
                else if (input === 'Close') {
                    break;
                }
            } else console.log('Argumento passado é inválido.')
        }else console.log('Comando inexistente.')
    }
}


//main
const main = async () => {
    //stub = client
    var packageDefinition = protoLoader.loadSync('../protos/movies.proto');
    var moviespackage = grpc.loadPackageDefinition(packageDefinition).moviespackage
    var stub = new moviespackage.Movies('localhost:7777', grpc.credentials.createInsecure());

    getInputs(stub)
}

main()
