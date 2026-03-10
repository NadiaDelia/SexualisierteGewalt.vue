<template>
    <footer class="footer-brava">
        <div class="footer-content">
            <div class="footer-col footer-left">
                <a href="https://www.brava-ngo.ch" target="_blank" rel="noopener noreferrer"><img class="footer-logo" src="/src/assets/Brava_Logo_U_de_weiss.svg" alt="Brava Logo" /></a><br /><br />
                <div class="footer-klein">© 2026 Nadia Delia Lanfranchi</div>
            </div>
            <div class="footer-col footer-center">
                <div class="footer-gross"><a class="footer-link"
                        href="https://www.brava-ngo.ch/de/unterstuetzen/jetzt-spenden" target="_blank"
                        rel="noopener noreferrer">Brava unterstützen</a></div>
            </div>
            <div class="footer-col footer-right">
                <div class="footer-gross">Brava folgen</div>
                <ul class="cross-list">
                    <li><a class="footer-link" href="https://www.brava-ngo.ch/de/newsletter" target="_blank"
                            rel="noopener noreferrer">Newsletter</a></li>
                    <li><a class="footer-link" href="https://www.instagram.com/brava.ngo/" target="_blank"
                            rel="noopener noreferrer">Instagram</a></li>
                    <li><a class="footer-link" href="https://www.linkedin.com/company/brava-ngo/" target="_blank"
                            rel="noopener noreferrer">LinkedIn</a></li>
                </ul>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'FooterBrava',
}
</script>

<style scoped>
.footer-brava {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    background: #000;
    color: #fff;
    z-index: 1000;
    padding: 0;
    font-family: 'PxGroteskPan', Arial, sans-serif;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.7s cubic-bezier(.4, 2, .6, 1);
}

.footer-brava.footer-visible {
    opacity: 1;
    pointer-events: auto;
    animation: footer-fade-in 1.2s cubic-bezier(.4, 2, .6, 1);
}

@keyframes footer-fade-in {
    0% {
        opacity: 0;
        transform: translateY(40px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.footer-content {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
    padding: 32px 32px 0 32px;
    gap: 32px;
}

.footer-col {
    flex: 1 1 0;
    min-width: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    height: 100%;
}

.footer-logo {
    height: 80px;
    margin-bottom: 8px;
    display: block;
}

.footer-gross {
    font-size: 1.4em;
    font-weight: 500;
    color: #fff;
}

.footer-klein {
    font-size: 1em;
    color: #fff;
    font-weight: 500;
    margin-top: auto;
    align-self: flex-start;
}

.footer-center {
    align-items: center;
    text-align: center;
    display: flex;
    flex-direction: column;
    width: 100%;
}

.footer-right {
    align-items: center;
    text-align: left;
    display: flex;
    flex-direction: column;
    width: 100%;
}

.footer-link {
    color: #fff;
    text-decoration: none;
    font-weight: 500;
}

.footer-link:visited,
.footer-link:active,
.footer-link:focus,
.footer-link:hover {
    color: #fff;
    text-decoration: none;
}

.cross-list {
    color: #fff;
    margin: 0.2em 0;
    list-style: none;
    padding: 0;
}

.cross-list li {
    color: #fff;
    margin: 0.1em 0;
    position: relative;
    padding-left: 2em;
}

.cross-list li::marker {
    content: "";
}

.cross-list li::before {
    content: "×" !important;
    position: absolute;
    color: #000;
    font-size: 1.4em;
    font-weight: 600;
    margin-bottom: 0.2em;
    color: #fff;
    margin-left: 0.4em;
    height: 20px;
    display: inline-block;
    text-align: left;
}
</style>
