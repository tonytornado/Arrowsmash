$(document).ready(
//    Fix things for when the song changes
    $('#song_title').onchange(function () {
        var clang = $('#song_title').val();
        checkSongValues(clang);
    })
);

function checkSongValues(songValue) {
    $.ajax({
        url: baseurl + "" + songValue,
        method: "GET",
        dataType: JSON,
        data: JSON,
        success: function (JSON) {
            console.log(JSON.data)
        }
    });
}