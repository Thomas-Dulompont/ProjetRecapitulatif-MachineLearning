const titreSpans = document.querySelectorAll('h1 span');

window.addEventListener('load', () => {

    const TL = gsap.timeline({paused: true});

    TL
    .staggerFrom(titreSpans, 1, {top: -50, opacity: 0, ease: "ease"}, 0.4)

    
    

    TL.play();
})