$(function() {
  var ISSPEECH = false;
  class SpeechRecognitionApi {
    constructor(options) {
      const SpeechToText =
          window.speechRecognition || window.webkitSpeechRecognition;
      this.speechApi = new SpeechToText();
      this.speechApi.continuous = false;
      this.speechApi.interimResults = false;
      this.speechApi.lang = "vi-VN";
      this.output =
          options.output ? options.output : document.createElement("div");
      this.speechApi.onresult = (event) => {
        console.log(event);
        var resultIndex = event.resultIndex;
        var transcript = event.results[resultIndex][0].transcript;

        console.log("transcript>>", transcript);
        console.log(this.output);
        send_message(transcript);
      };

      this.speechApi.onstart = function() {
        $("#speech-icon").text("mic_none");
        ISSPEECH = true;
      };

      this.speechApi.onspeechend = function() {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
      };

      this.speechApi.onnomatch = function() {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
        generate_message("Bạn có thể nói rõ hơn được không?", 'user');
        this.stop();
      };
      this.speechApi.onaudioend = function() {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
      };
    }
    init() { this.speechApi.start(); }
    stop() { this.speechApi.stop(); }
  }

  var INDEX = 1;
  $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val();
    send_message(msg);
  });

  // Tag change event
  $("#tag").change(function() {
    var newtag = $("#tag").text();
    $.get("/get-img", {tag : newtag}).done(function(data) {
      $("#prepare-paper").empty();
      $("#to-khai").empty();
      if (Object.keys(data).length === 0) {
        return 0;
      }

      var str = "";
      var tokhai = "";
      for (const element of data) {
        if (element.title == "to_khai") {
          tokhai += "<div class='media full'> ";
          tokhai += "<div class = 'layer'>";
          tokhai += "<p>" +
                    "Tờ khai " + newtag + "</p>" +
                    "</div>";
          tokhai += "<img " +
                    "src='" + element.src + "' alt='' />" +
                    "</div>";
          tokhai += "\n";
        } else {
          str += "<div class='media'> ";
          str += "<div class = 'layer'>";
          str += "<p>" + element.title + "</p>" +
                 "</div>";
          str += "<img " +
                 "src='" + element.src + "' alt='' />" +
                 "</div>";
          str += "\n";
        }
      }

      $("#prepare-paper").append(str);
      $("#to-khai").append(tokhai);

      var element = document.querySelectorAll("img");
      Intense(element);

      $(".layer").on("click", function() {
        var oldtag = $("#tag").text();
        var msg = $(this).text();
        console.log(msg);
        generate_message(msg, "self");

        $.get("/get", {msg : msg, oldtag : oldtag}).done(function(data) {
          var response = linkify(String(data.response));

          text2Speech.text = clean_url(response);
          speechSynthesis.speak(text2Speech);

          generate_message(response, "user");
        });
      });
    });
  });
  // Text to speech
  var text2Speech = new SpeechSynthesisUtterance();
  text2Speech.lang = "vi-VN";

  // Speech recoginition
  var speech = new SpeechRecognitionApi({});

  $("#speech").click(function(e) {
    e.preventDefault();

    if (!ISSPEECH) {
      speech.init();
      $("#speech-icon").text("mic_none");
      ISSPEECH = true;
    } else {
      speech.stop();
      $("#speech-icon").text("mic_off");
      ISSPEECH = false;
    }
  });

  function generate_message(msg, type) {
    INDEX++;
    var str = "";
    str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';
    if (type != "self") {
      str += '          <span class="msg-avatar">';
      str += '            <img src="/static/img/chatbot.jpg">';
      str += "          </span>";
    }

    str += '          <div class="cm-msg-text">';
    str += msg;
    str += "          </div>";
    str += "        </div>";
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX).hide().fadeIn(300);
    if (type == "self") {
      $("#chat-input").val("");
    }
    $(".chat-logs")
        .stop()
        .animate({scrollTop : $(".chat-logs")[0].scrollHeight}, 1200);
  }

  function generate_button_message(msg, buttons) {
    /* Buttons should be object array
        [
          {
            name: 'Existing User',
            value: 'existing'
          },
          {
            name: 'New User',
            value: 'new'
          }
        ]
      */
    INDEX++;
    var btn_obj =
        buttons
            .map(function(button) {
              return (
                  '              <li class="button"><a href="javascript:;" class="btn btn-primary chat-btn" chat-value="' +
                  button.value + '">' + button.name + "</a></li>");
            })
            .join("");
    var str = "";
    str += "<div id='cm-msg-" + INDEX + '\' class="chat-msg user">';
    str += '          <span class="msg-avatar">';
    str +=
        '            <img src="https://image.crisp.im/avatar/operator/196af8cc-f6ad-4ef7-afd1-c45d5231387c/240/?1483361727745">';
    str += "          </span>";
    str += '          <div class="cm-msg-text">';
    str += msg;
    str += "          </div>";
    str += '          <div class="cm-msg-button">';
    str += "            <ul>";
    str += btn_obj;
    str += "            </ul>";
    str += "          </div>";
    str += "        </div>";
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX).hide().fadeIn(300);
    $(".chat-logs")
        .stop()
        .animate({scrollTop : $(".chat-logs")[0].scrollHeight}, 1000);
    $("#chat-input").attr("disabled", true);
  }

  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, "self");
  });

  $("#chat-circle").click(function() {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");
  });

  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");
  });

  function send_message(msg) {
    var oldtag = $("#tag").text();
    if (msg.trim()) {
      generate_message(msg, "self");

      $.get("/get", {msg : msg, oldtag : oldtag}).done(function(data) {
        console.log(data);
        // myData = JSON.parse(data)
        var response = linkify(String(data.response));
        var tag = data.tag;
        if (tag != "lời chào" && tag != "cảm xúc" && tag != oldtag &&
            tag != "none") {
          $("#tag").text(tag).trigger("change");
        }

        text2Speech.text = clean_url(response);
        speechSynthesis.speak(text2Speech);

        generate_message(response, "user");
      });
    }
  }

  function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    // URLs starting with http://, https://, or ftp://
    replacePattern1 =
        /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1,
                                     '<a href="$1" target="_blank">$1</a>');

    // URLs starting with "www." (without // before it, or it'd re-link the ones
    // done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(
        replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    // Change email addresses to mailto:: links.
    replacePattern3 =
        /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText =
        replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
  }
  function clean_url(inputText) {
    inputText = String(inputText)
    return inputText.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');
  }

  /////==========script end point==============////
});
