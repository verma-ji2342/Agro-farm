$("#openJarvis").click(() => {
    $("#openJarvis").addClass("hidden");
    $(".chat-container").removeClass("hidden");
    $("#formContainer").removeClass("hidden");
});

$("#jarvis").submit(e => {
  e.preventDefault();
  $(".chat-container").append($("<div></div>").text($("#request").val()).css({"max-width": "70%", "padding": "1rem", "background-color": "rgb(251 146 60)", "width": "min-content", "align-self": "flex-end"}));
  axios.post('http://localhost:5000/jarvis', {"data": $("#request").val()})
    .then((res) => {
        let newMessage = $("<div></div>").text(res.data.response).css({"max-width": "70%", "padding": "1rem", "background-color": "rgb(251 146 60)", "width": "min-content"});
        $(".chat-container").append(newMessage);
    })
    .catch((error) => console.log(error));
});

$("#hj").submit(e => {
     e.preventDefault();
      axios.post('http://localhost:5000/help_jarvis', {"data_q": $("#hj_q").val(), "data_a": $("#hj_a").val()})
        .then((res) => {
            console.log(res);
        })
        .catch((error) => console.log(error));
});
