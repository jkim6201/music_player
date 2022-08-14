console.log("page loaded...");

function message(element){
    let spotifyApi = `https://open.spotify.com/embed/track/${element.dataset.index}?utm_source=generator`
    document.getElementById("iframe").src  = spotifyApi
    document.getElementById("track_id").value = element.dataset.index
}
