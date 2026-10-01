const DEMO_SHAPES = {
  star: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 5 L64 35 L97 38 L72 61 L79 94 L50 77 L21 94 L28 61 L3 38 L36 35 Z" fill="black" />
  </svg>`,
  
  heart: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 85 C50 85, 10 55, 10 30 C10 15, 25 5, 40 15 C50 25, 50 25, 50 25 C50 25, 50 25, 60 15 C75 5, 90 15, 90 30 C90 55, 50 85, 50 85 Z" fill="black" />
  </svg>`,
  
  moon: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M70 10 A40 40 0 1 0 90 80 A30 30 0 1 1 70 10 Z" fill="black" />
  </svg>`,
  
  tree: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 10 L80 40 L65 40 L90 70 L60 70 L65 95 L35 95 L40 70 L10 70 L35 40 L20 40 Z" fill="black" />
  </svg>`,
  
  butterfly: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 30 C60 10, 95 10, 95 40 C95 55, 75 75, 50 90 C25 75, 5 55, 5 40 C5 10, 40 10, 50 30 Z" fill="black" />
  </svg>`,
  
  dragon: `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 90 C10 80, 20 60, 40 50 C30 45, 15 45, 10 30 C20 30, 35 40, 45 45 C50 30, 45 15, 60 10 C65 25, 55 35, 55 45 C75 40, 90 25, 95 40 C85 50, 65 50, 60 55 C70 70, 90 85, 75 95 C65 85, 60 70, 50 65 C40 80, 30 95, 20 90 Z" fill="black" />
  </svg>`,
  
  probharath: `<svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <!-- Elephant Body & Head -->
    <path d="M80 35 C80 20 65 10 45 10 C30 10 18 18 16 30 L16 50 C16 55 20 60 25 60 C30 60 32 55 32 50 C32 45 30 40 25 40 L22 40 L22 30 C22 25 30 18 45 18 C55 18 65 25 65 35 L65 75 L50 75 L50 55 L40 55 L40 75 L25 75 L25 65 L15 65 L15 85 L45 85 L45 65 L55 65 L55 85 L75 85 L75 45 L85 40 L80 35 Z" fill="black"/>
    <path d="M16 50 C16 65 25 75 35 75 C38 75 40 72 40 70 C40 68 38 65 35 65 C30 65 25 60 25 50 Z" fill="black"/>
    <path d="M28 55 L15 65 L20 70 L30 60 Z" fill="white"/>
    <text x="50" y="98" font-family="'Orbitron', sans-serif" font-size="14" font-weight="bold" fill="black" text-anchor="middle">ProBharath</text>
  </svg>`,

  samurai: `<svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="85" width="100" height="15" fill="black"/>
    <path d="M 30 35 L 70 35 L 50 25 Z" fill="black"/>
    <path d="M 45 35 L 55 35 L 60 60 L 40 60 Z" fill="black"/>
    <path d="M 40 60 L 25 85 L 40 85 L 50 65 L 60 85 L 75 85 L 60 60 Z" fill="black"/>
    <rect x="15" y="48" width="70" height="2" fill="black"/>
    <rect x="60" y="45" width="35" height="4" transform="rotate(25 60 45)" fill="black"/>
    <circle cx="20" cy="20" r="12" fill="black"/>
  </svg>`,

  lotus: `<svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M50 85 C30 60 35 25 50 10 C65 25 70 60 50 85 Z" fill="black"/>
    <path d="M50 85 C20 75 5 45 20 30 C30 20 45 40 50 85 Z" fill="black"/>
    <path d="M50 85 C10 85 0 65 5 50 C10 35 30 45 50 85 Z" fill="black"/>
    <path d="M50 85 C80 75 95 45 80 30 C70 20 55 40 50 85 Z" fill="black"/>
    <path d="M50 85 C90 85 100 65 95 50 C90 35 70 45 50 85 Z" fill="black"/>
    <circle cx="50" cy="75" r="5" fill="white"/>
  </svg>`,

  cityscape: `<svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="40" width="15" height="60" fill="black"/>
    <rect x="22" y="20" width="20" height="80" fill="black"/>
    <rect x="45" y="50" width="10" height="50" fill="black"/>
    <rect x="58" y="10" width="15" height="90" fill="black"/>
    <rect x="76" y="30" width="18" height="70" fill="black"/>
    <rect x="26" y="25" width="4" height="6" fill="white"/>
    <rect x="34" y="25" width="4" height="6" fill="white"/>
    <rect x="26" y="35" width="4" height="6" fill="white"/>
    <rect x="34" y="35" width="4" height="6" fill="white"/>
    <rect x="62" y="15" width="6" height="8" fill="white"/>
    <rect x="62" y="28" width="6" height="8" fill="white"/>
    <circle cx="85" cy="15" r="8" fill="black"/>
  </svg>`,

  wolf: `<svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40" fill="black"/>
    <path d="M 50 90 C 20 90 10 70 10 50 C 10 30 30 10 50 10 C 70 10 90 30 90 50 C 90 70 80 90 50 90 Z" fill="black"/>
    <path d="M 40 90 L 30 65 L 45 55 L 55 60 L 60 50 L 50 40 L 40 45 L 35 30 L 45 20 L 65 30 L 70 45 L 60 50 L 65 65 L 55 90 Z" fill="white"/>
  </svg>`
};

function getDemoImage(key) {
  return DEMO_SHAPES[key] || DEMO_SHAPES['star'];
}
