----------------------
Ping Monitor 
----------------------
\\executa setup
python setup.py build


----------------------
Descrição:
----------------------
O Ping Monitor é um aplicativo simples que permite 
monitorar o status de dispositivos na rede usando o protocolo ICMP (Ping).
Ele exibe o status de cada dispositivo em uma interface gráfica e 
alerta quando um dispositivo para de responder ao ping.


----------------------
Instruções de Uso
----------------------
Adicionar Dispositivos:
Clique no botão "Add Device".
Insira o endereço IP do dispositivo que você deseja monitorar.
Clique em "OK" para confirmar a adição do dispositivo.

Remover Dispositivos:
Selecione o dispositivo na tabela.
Clique no botão "Remove Selected" para remover o dispositivo da lista de monitoramento.

Iniciar Monitoramento:
Clique no botão "Start Monitoring" para iniciar o monitoramento dos dispositivos.
O status de cada dispositivo será atualizado na tabela a cada segundo.

Parar Monitoramento:
Clique no botão "Stop Monitoring" para interromper o monitoramento dos dispositivos.
O status dos dispositivos será limpo na tabela.

Alerta de Dispositivos Não Respondendo:
Quando um dispositivo para de responder ao ping, um alerta por email será enviado 
(para tihbaextrema@gmail.com). Verifique a seção "Configurações de Email" no 
código para personalizar o remetente, destinatário e servidor SMTP.


----------------------
Versão do Aplicativo:
----------------------
A versão atual do aplicativo é exibida na parte inferior direita da janela.


----------------------
Lógica do Programa.
----------------------
O Ping Monitor utiliza threads para executar o monitoramento de dispositivos e a 
interface gráfica. A classe MonitorThread é responsável por realizar o ping em intervalos 
regulares para verificar o status dos dispositivos. A interface gráfica é criada usando a 
biblioteca Tkinter.

Os dispositivos adicionados são exibidos em uma tabela, onde o status de 
cada dispositivo é atualizado em tempo real. Quando um dispositivo para de
responder ao ping, um alerta por email é enviado para o endereço especificado 
nas configurações.
