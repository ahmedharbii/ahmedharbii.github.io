function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    camera.position.z = 50;

    const particleCount = 100;
    const particles = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const velocities = [];

    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 100;
        positions[i + 1] = (Math.random() - 0.5) * 100;
        positions[i + 2] = (Math.random() - 0.5) * 100;
        velocities.push({
            x: (Math.random() - 0.5) * 0.02,
            y: (Math.random() - 0.5) * 0.02,
            z: (Math.random() - 0.5) * 0.02
        });
    }

    particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const particleMaterial = new THREE.PointsMaterial({
        color: 0x57cc99,
        size: 0.5,
        transparent: true,
        opacity: 0.8
    });

    const particleSystem = new THREE.Points(particles, particleMaterial);
    scene.add(particleSystem);

    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x57cc99,
        transparent: true,
        opacity: 0.2
    });
    const lines = [];

    const mouse = { x: 0, y: 0 };
    document.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    function updateParticleColors() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const color = isDark ? 0x90e0ef : 0x57cc99;
        particleMaterial.color.setHex(color);
        lineMaterial.color.setHex(color);
    }

    const themeObserver = new MutationObserver(updateParticleColors);
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    updateParticleColors();

    function animate() {
        requestAnimationFrame(animate);

        const positions = particles.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3] += velocities[i].x;
            positions[i3 + 1] += velocities[i].y;
            positions[i3 + 2] += velocities[i].z;

            if (Math.abs(positions[i3]) > 50) velocities[i].x *= -1;
            if (Math.abs(positions[i3 + 1]) > 50) velocities[i].y *= -1;
            if (Math.abs(positions[i3 + 2]) > 50) velocities[i].z *= -1;
        }
        particles.attributes.position.needsUpdate = true;

        lines.forEach(line => scene.remove(line));
        lines.length = 0;

        for (let i = 0; i < particleCount; i++) {
            for (let j = i + 1; j < particleCount; j++) {
                const i3 = i * 3;
                const j3 = j * 3;
                const dx = positions[i3] - positions[j3];
                const dy = positions[i3 + 1] - positions[j3 + 1];
                const dz = positions[i3 + 2] - positions[j3 + 2];
                const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

                if (distance < 15) {
                    const lineGeometry = new THREE.BufferGeometry();
                    const linePositions = new Float32Array([
                        positions[i3], positions[i3 + 1], positions[i3 + 2],
                        positions[j3], positions[j3 + 1], positions[j3 + 2]
                    ]);
                    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
                    const line = new THREE.Line(lineGeometry, lineMaterial);
                    scene.add(line);
                    lines.push(line);
                }
            }
        }

        particleSystem.rotation.y += 0.001 + mouse.x * 0.001;
        particleSystem.rotation.x += 0.001 + mouse.y * 0.001;

        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

document.addEventListener('DOMContentLoaded', initParticles);
