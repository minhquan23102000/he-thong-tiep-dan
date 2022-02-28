$(function () {
  var ISSPEECH = false;
  class SpeechRecognitionApi {
    constructor(options) {
      const SpeechToText =
        window.speechRecognition || window.webkitSpeechRecognition;
      this.speechApi = new SpeechToText();
      this.speechApi.continuous = false;
      this.speechApi.interimResults = false;
      this.speechApi.lang = "vi-VN";
      this.output = options.output
        ? options.output
        : document.createElement("div");
      this.speechApi.onresult = (event) => {
        var resultIndex = event.resultIndex;
        var transcript = event.results[resultIndex][0].transcript;

        send_message(transcript);
      };

      this.speechApi.onstart = function () {
        $("#speech-icon").text("mic_none");
        ISSPEECH = true;
      };

      this.speechApi.onspeechend = function () {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
      };

      this.speechApi.onnomatch = function () {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
        generate_message("Bạn có thể nói rõ hơn được không?", "user");
        this.stop();
      };
      this.speechApi.onaudioend = function () {
        $("#speech-icon").text("mic_off");
        ISSPEECH = false;
      };
    }
    init() {
      this.speechApi.start();
    }
    stop() {
      this.speechApi.stop();
    }
  }

  var INDEX = 1;
  $("#chat-submit").click(function (e) {
    e.preventDefault();
    var msg = $("#chat-input").val();
    send_message(msg);
  });

  // Tag change event
  $("#tag").change(function () {
    var newtag = $("#tag").text();
    $.get("/get-img", { tag: newtag }).done(function (data) {
      $("#img-guide").empty();
      $("#to-khai").empty();
      $("#img-detail").empty();
      if (Object.keys(data.paper).length === 0) {
        return 0;
      }

      var str = "";
      var tokhai = "";
      var modal = "";
      for (var i = 0; i < data.paper.length; i += 2) {
        // Init a rows
        str += "<div class='row row-0-gutter'> ";
        for (var j = i; j < i + 2 && j < data.paper.length; j++) {
          // Init a columns
          str += "<div class='col-md-6 col-0-gutter'> ";

          //Init image container
          str += "<div class='ot-portfolio-item'> ";
          str += "<figure class='effect-bubba'> ";
          //Add image data
          str += "<img src='" + data.paper[j].src + "' ";
          str += " alt='website template image' class='img-responsive'></img>";
          //Add caption
          str += "<figcaption> ";
          str += "<h2> " + data.paper[j].title + "</h2> ";
          str += "<p> Chi tiết </p> ";
          str +=
            "<a href='javascript:void(0)' data-toggle='modal' data-target='#Modal-" +
            j +
            "'>View more</a>";
          str += "</figcaption> ";

          //Close img header
          str += " </div> ";
          str += " </figure> ";
          //Close a columns
          str += " </div> ";

          //generate modal
          modal += generate_modal(j, data.paper[j]);
        }

        //Close a row
        str += " </div>";
      }

      tokhai += "<img src='" + data.to_khai.src + "' ";
      tokhai += " alt='website template image' class='img-responsive'></img>";

      // Apply data to client view
      $("#img-guide").append(str);
      $("#to-khai").append(tokhai);
      $("#img-detail").append(modal);
      $("#tag-description").text(data.description);
    });
  });

  function generate_modal(index, data) {
    var str =
      "<div class='modal fade' id ='Modal-" +
      index +
      "' tabindex ='-1' role='dialog' aria-labelledby='Modal-label-" +
      index +
      "'>";
    str += " <div class='modal-dialog' role = 'document'>";
    str += " <div class = 'modal-content'>";
    str += " <div class = 'modal-header'>";
    str +=
      " <button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button>";
    str += " </div>";
    str +=
      " <div class ='modal-body'> <img src = '" +
      data.src +
      "' alt = 'website template image' class='img-responsive'>";
    str += " <p> " + data.description + "<p>";
    str += " </div>";
    str +=
      " <div class='modal-footer'> <button type='button' class='btn btn-default' data-dismiss='modal'>Close</button> </div>";
    str += " </div>";
    str += " </div>";
    str += " </div>";
    str += " ";
    return str;
  }

  // Text to speech
  var text2Speech = new SpeechSynthesisUtterance();
  text2Speech.lang = "vi-VN";
  var voices = [];

  window.speechSynthesis.onvoiceschanged = function() {
    var hhvoices = window.speechSynthesis.getVoices();
    voices = [];
    

    for (var i = 0; i < hhvoices.length; i++) {
      if (hhvoices[i].lang == "vi-VN") { 
        console.log(i + " " + hhvoices[i].name + " " + hhvoices[i].default);
        voices.push(hhvoices[i]);
      }
      
    }
    console.log("Voices " + voices.length)
  };

  

   
  // Speech recoginition
  var speech = new SpeechRecognitionApi({});

  $("#speech").click(function (e) {
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
    //Clean next questions
    $(".next-msg").remove();

    INDEX++;
    var str = "";
    str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';

    str += '          <div class="cm-msg-text">';
    str += msg;
    str += "          </div>";
    str += "        </div>";

    $(".chat-logs").append(str);

    $("#cm-msg-" + INDEX)
      .hide()
      .fadeIn(300);

    if (type == "self") {
      $("#chat-input").val("");
    }

    $(".chat-logs")
      .stop()
      .animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1200);
  }

  function generate_next_questions(next_questions) {
    var str = "";
    var type = "self";
    for (let index = 0; index < next_questions.length; index++) {
      str +=
        "<div id='cm-msg-" +
        (INDEX + 1 + index) +
        "' class=\"next-msg " +
        type +
        '">';

      str += '          <div class="next-msg-text">';
      str += next_questions[index];
      str += "          </div>";
      str += "        </div>";
    }

    $(".chat-logs").append(str);

    $("#cm-msg-" + INDEX + 1)
      .hide()
      .fadeIn(300);
    $("#cm-msg-" + INDEX + 2)
      .hide()
      .fadeIn(400);
    $("#cm-msg-" + INDEX + 3)
      .hide()
      .fadeIn(500);

    $(".chat-logs")
      .stop()
      .animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1200);

    //On click next questions event
    $(".next-msg-text").click(function (e) {
      e.preventDefault();

      var text = $(this).text();
      send_message(text);
    });
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
    var btn_obj = buttons
      .map(function (button) {
        return (
          '              <li class="button"><a href="javascript:;" class="btn btn-primary chat-btn" chat-value="' +
          button.value +
          '">' +
          button.name +
          "</a></li>"
        );
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
    $("#cm-msg-" + INDEX)
      .hide()
      .fadeIn(300);
    $(".chat-logs")
      .stop()
      .animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    $("#chat-input").attr("disabled", true);
  }

  $(document).delegate(".chat-btn", "click", function () {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, "self");
  });

  $("#chat-circle").click(function () {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");
  });

  $(".chat-box-toggle").click(function () {
    $("#chat-circle").toggle("scale");
    $(".chat-box").toggle("scale");
  });

  function send_message(msg) {
    var oldtag = $("#tag").text();
    if (msg.trim()) {
      generate_message(msg, "self");

      $.get("/get", { msg: msg, oldtag: oldtag }).done(function (data) {
        console.log(data);
        // myData = JSON.parse(data)
        var response = linkify(String(data.response));
        var tag = data.tag;
        var next_questions = data.next_questions;

        if (
          tag != "lời chào" &&
          tag != "cảm xúc" &&
          tag != oldtag &&
          tag != "none"
        ) {
          $("#tag").text(tag).trigger("change");
        }

        text2Speech.text = clean_url(response);
        speechSynthesis.cancel();
        speechSynthesis.speak(text2Speech);

        generate_message(response, "user");
        setTimeout(function () {
          generate_next_questions(next_questions);
        }, 1100);
      });
    }
  }

  function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    // URLs starting with http://, https://, or ftp://
    replacePattern1 =
      /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(
      replacePattern1,
      '<a href="$1" target="_blank">$1</a>'
    );

    // URLs starting with "www." (without // before it, or it'd re-link the ones
    // done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(
      replacePattern2,
      '$1<a href="http://$2" target="_blank">$2</a>'
    );

    // Change email addresses to mailto:: links.
    replacePattern3 =
      /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(
      replacePattern3,
      '<a href="mailto:$1">$1</a>'
    );

    return replacedText;
  }
  function clean_url(inputText) {
    inputText = String(inputText);
    return inputText.replace(/(?:https?|ftp):\/\/[\n\S]+/g, "");
  }

  /////==========script end point==============////
});
