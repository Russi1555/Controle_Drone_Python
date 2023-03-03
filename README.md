<h1>Controle_Drone_Python</h1>

<h2>Instalação de Bibliotecas</h2>
<ul>
  <li>python3 -m pip install dronekit</li>
  <li>python3 -m pip install dronekit-sitl</li>
  <li>python3 -m pip install pyserial</li>
  <li>python3 -m pip install serial</li>
</ul>

<h2>Inicialização com simulador</h2>
<ol>
  <li>Executar controle_drone_python.py</li>
  <li>Aguardar a inicialização do QGroundControl</li>
  <li>Abrir Application Settings</li>
  <li>Entrar no menu Comm Links</li>
  <li>Clicar em "Add"</li>
  <li>
      <ul>
      <li>Name: (Qualquer um)</li>
      <li>Caixas desmarcadas</li>
      <li>Type: TCP</li>
      <li>Server Address: 127.0.0.1</li>
      <li>Port: 5762</li>
      </ul> 
  </li>
</ol>

<h2>Controle</h2>
<ul>
  <li> ↑ : Movimenta drone para frente </li>
  <li> ↓ : Movimenta drone para trás </li>
  <li> → : Movimenta drone para direita </li>
  <li> ← : Movimenta drone para esquerda </li>
  <li> + : Aumenta a velocidade do drone </li>
  <li> - : Diminiu a velocidade do drone </li>
  <li> e : Rotaciona o drone 10° sentido horário </li>
  <li> q : Rotaciona o drone 10° sentido anti-horário </li>
  <li> [ : Eleva altitude em aproximadamente 1 metro </li>
  <li> ] : Reduz altitude em aproximadamente 1 metro </li>
</ul>

<h2>Documentação das mensagems</h2>
<ul>
  <li>https://mavlink.io/en/messages/common.html</li>
</ul>
