let n = document.getElementById("logIn");
      let d = document.getElementById("welcome");
      let g = document.getElementById("nick");
      n.style.visibility = 'hidden';
      $('.message').prop('disabled', true);
      function connect(){
          if (g.value.trim() === "" || g.value.trim() === "polzowatel"){
              document.getElementById("Error").textContent="Not correct input data, Try again";
          }
          else{
            n.style.visibility = 'visible';
            d.style.visibility = 'hidden';
            goi()
          }
      }
      function goi(){
        let socket = new WebSocket("ws://localhost");
        socket.onopen = function () {
          socket.send(g.value.trim());
          document.querySelector("textarea").addEventListener('keyup', function (e) {
            if (e.keyCode === 13) {
              if (this.value.trim() === "") {
                return false;
              }
              socket.send(this.value.trim());
              this.value = "";
            }
          });
        };
        socket.onerror = function () {
          console.log('Ошибка при подключении');
        };
        let p = "";
        socket.onmessage = function (e) {
          $('.message').val($.trim($('.message').val() + '\n' + e.data));
          var psconsole = $('.message');
          if(psconsole.length)
              psconsole.scrollTop(psconsole[0].scrollHeight - psconsole.height());
        };
      }