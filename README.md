O comando utilizado para reproduzir a carga de trabalho é o seguinte: 

*./mqtt-benchmark--broker tcp://<IP-da-VM-vítima>:1883--count 100--size <Tamanho> --clients 100--qos 2--format text*

onde é necessário substituir o parâmetro **<IP-da-VM-vítima>** pelo endereço IP da VM vítima e o parâmetro **Tamanho** pelo tamanho da mensagem em bytes (i.e., _payload_ do pacote). 
