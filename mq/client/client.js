/*
Este código implementa a parte Cliente de um programa de fila de mensagens que coleta,
classifica e distribui tweets de acordo com tópicos selecionados pelo cliente.

Autores:
  - Ryan Lazaretti @ryanramos01
  - Caio Miglioli @caiomiglioli

Data de Criação: 30 de Maio de 2023
Ultima alteração: 30 de Maio de 2023
*/

const amqp = require('amqplib/callback_api');
const prompt = require('prompt-sync')();

// Estabelecendo uma conexão com o servidor RabbitMQ rodando no endereço 'amqp://localhost'
amqp.connect('amqp://localhost', function(error0, connection) {
    // Se houver algum erro na conexão, o erro será lançado
    if (error0) {
        throw error0;
    }
    
    // Criando um canal de comunicação após a conexão ser estabelecida
    connection.createChannel(async function(error1, channel) {
        // Se houver algum erro na criação do canal, o erro será lançado
        if (error1) {
            throw error1;
        }

        // Usando o prompt para obter a entrada do usuário do terminal
        const input = prompt('Which topics to follow? > ');

        // Dividindo a entrada do usuário em várias filas
        const queues = input.split(' ');
        // Iterando sobre todas as filas
        for(let i = 0; i < queues.length; i++){



            // Garantindo que a fila esteja disponível para enviar mensagens
            // channel.assertQueue(queues[i], {
            //     durable: false
            // });
            

            const topic = queues[i]

            // Declara o exchange
            channel.assertExchange('classified-tweets', 'topic', { durable: false });

            // Cria uma fila exclusiva
            const result = channel.assertQueue('', { exclusive: true });
            const queue = result.queue;

            // Faz o bind da fila com o tópico
            const routingKey = topic;
            channel.bindQueue(queue, 'classified-tweets', routingKey);



            // Logando uma mensagem indicando que o cliente está esperando por mensagens
            console.log(" [*] Esperando mensagens de %s. Para sair pressione CTRL+C", queues[i]);

            // Consumindo mensagens da fila especificada. Quando uma mensagem é recebida, ela é logada no console
            channel.consume(queue, (msg) => {
              // Converte a string JSON recebida em um objeto JavaScript usando JSON.parse()
              let msgObj = JSON.parse(msg.content.toString());

              // Cria uma string formatada
              let output = `
                  [x] Mensagem recebida de ${queues[i]}:
                  Tweet: ${msgObj.tweet} 
                  At: @${msgObj.at}
                  Date: ${new Date(msgObj.date * 1000).toLocaleString()} 
              `;

              // Imprime a string formatada no console
              console.log(output);
          }, {
              // Definição para que as mensagens não sejam reconhecidas automaticamente pelo consumidor
              noAck: true
          });
      }
  });
});

