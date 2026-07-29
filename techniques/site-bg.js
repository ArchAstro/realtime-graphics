/**
 * Subtle WebGL backdrop — visible atmosphere, never competes with text.
 * Content sits on opaque frosted panels (see shared.css / prompt-page.css).
 */
(function () {
  function enableStaticFallback() {
    document.documentElement.classList.add("has-site-bg", "site-bg-static");
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    enableStaticFallback();
    return;
  }
  if (document.getElementById("site-bg")) return;

  const canvas = document.createElement("canvas");
  canvas.id = "site-bg";
  canvas.setAttribute("aria-hidden", "true");
  Object.assign(canvas.style, {
    position: "fixed",
    top: "0",
    left: "0",
    width: "100vw",
    height: "100vh",
    zIndex: "-1",
    pointerEvents: "none",
    display: "block",
  });
  document.documentElement.appendChild(canvas);
  document.documentElement.classList.add("has-site-bg");

  const gl =
    canvas.getContext("webgl", {
      alpha: false,
      antialias: false,
      depth: false,
      powerPreference: "low-power",
    }) || canvas.getContext("experimental-webgl");

  if (!gl) {
    canvas.remove();
    enableStaticFallback();
    return;
  }

  const vsSource = `
    attribute vec2 a_pos;
    void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }
  `;

  // Dim, slow, edge-weighted — center stays dark for readability
  const fsSource = `
    precision mediump float;
    uniform vec2 u_res;
    uniform float u_time;

    void main() {
      vec2 uv = gl_FragCoord.xy / u_res;
      vec2 p = (gl_FragCoord.xy - 0.5 * u_res) / min(u_res.x, u_res.y);
      float t = u_time * 0.12;

      // Near-black base
      vec3 col = vec3(0.04, 0.05, 0.09);

      // Soft edge glows only (low intensity)
      vec2 c1 = vec2(-0.55 + 0.08 * sin(t * 0.7), 0.45 + 0.06 * cos(t * 0.5));
      col += vec3(0.12, 0.28, 0.48) * exp(-dot(p - c1, p - c1) * 1.6) * 0.45;

      vec2 c2 = vec2(0.6 + 0.07 * cos(t * 0.55), -0.35 + 0.08 * sin(t * 0.4));
      col += vec3(0.28, 0.12, 0.38) * exp(-dot(p - c2, p - c2) * 1.5) * 0.35;

      vec2 c3 = vec2(0.1 + 0.1 * sin(t * 0.35), -0.65);
      col += vec3(0.35, 0.18, 0.08) * exp(-dot(p - c3, p - c3) * 1.8) * 0.28;

      // Very gentle vertical wash
      col += vec3(0.02, 0.04, 0.08) * (1.0 - uv.y) * 0.35;

      // Strong center darkening so text regions stay clear
      float center = smoothstep(0.15, 1.1, length(p * vec2(0.75, 0.95)));
      col *= 0.35 + 0.65 * center;

      // Tiny grain
      float g = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);
      col += (g - 0.5) * 0.012;

      col = clamp(col, 0.03, 0.55);
      gl_FragColor = vec4(col, 1.0);
    }
  `;

  function compile(type, src) {
    const sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.error("[site-bg]", gl.getShaderInfoLog(sh));
      return null;
    }
    return sh;
  }

  const vs = compile(gl.VERTEX_SHADER, vsSource);
  const fs = compile(gl.FRAGMENT_SHADER, fsSource);
  if (!vs || !fs) {
    canvas.remove();
    enableStaticFallback();
    return;
  }

  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    canvas.remove();
    enableStaticFallback();
    return;
  }
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1]),
    gl.STATIC_DRAW
  );
  const aPos = gl.getAttribLocation(prog, "a_pos");
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

  const uRes = gl.getUniformLocation(prog, "u_res");
  const uTime = gl.getUniformLocation(prog, "u_time");

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = Math.max(1, Math.floor(window.innerWidth * dpr));
    const h = Math.max(1, Math.floor(window.innerHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
  }

  let raf = 0;
  let last = 0;
  function frame(ts) {
    raf = requestAnimationFrame(frame);
    if (ts - last < 40) return;
    last = ts;
    resize();
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, ts * 0.001);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  resize();
  gl.uniform2f(uRes, canvas.width, canvas.height);
  gl.uniform1f(uTime, 0);
  gl.drawArrays(gl.TRIANGLES, 0, 6);
  raf = requestAnimationFrame(frame);

  window.addEventListener("beforeunload", () => cancelAnimationFrame(raf), {
    once: true,
  });
  window.__SITE_BG__ = { version: 4, gl: true };
})();
