{
  cross ? false,
}:
let
  nixconfig = builtins.getFlake "github:death916/nixconfig";

  pkgs =
    if cross then
      import nixconfig.inputs.nixpkgs {
        system = "x86_64-linux";
        crossSystem = {
          config = "aarch64-unknown-linux-gnu";
        };
      }
    else
      nixconfig.inputs.nixpkgs.legacyPackages.x86_64-linux;

  buildPkgs = nixconfig.inputs.nixpkgs.legacyPackages.x86_64-linux;

  unstable =
    if cross then
      import nixconfig.inputs.nixpkgs-unstable {
        system = "x86_64-linux";
        crossSystem = {
          config = "aarch64-unknown-linux-gnu";
        };
      }
    else
      nixconfig.inputs.nixpkgs-unstable.legacyPackages.x86_64-linux;

  rustTarget = if cross then "aarch64-unknown-linux-gnu" else "x86_64-unknown-linux-gnu";
in
pkgs.mkShell {
  nativeBuildInputs = with buildPkgs; [
    python313Packages.uv
    python313Packages.ninja
    python313Packages.numpy
    bun
    unstable.rustc
    unstable.cargo
    unstable.rust-analyzer
    unstable.rustfmt
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcb
    pkgs.alsa-lib
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.fontconfig
    pkgs.freetype
    pkgs.mesa
    pkgs.libGL
    pkgs.libglvnd
    pkgs.glib
    pkgs.vulkan-loader
    pkgs.vulkan-headers
    unstable.clippy
    # CEF Dependencies (System level)
    pkgs.nss
    pkgs.nspr
    pkgs.atk
    pkgs.at-spi2-atk
    pkgs.at-spi2-core
    pkgs.dbus
    pkgs.cups
    pkgs.libdrm
    pkgs.libgbm
    pkgs.libxshmfence
    pkgs.udev
    pkgs.expat
    pkgs.cairo
    pkgs.pango
    pkgs.systemd
    pkgs.xorg.libX11
    pkgs.xorg.libXcomposite
    pkgs.xorg.libXdamage
    pkgs.xorg.libXext
    pkgs.xorg.libXfixes
    pkgs.xorg.libXrandr
    pkgs.xorg.libXrender
    pkgs.xorg.libXtst
    pkgs.xorg.libxcb
    pkgs.pciutils
    pkg-config
    clippy
  ];

  buildInputs = with pkgs; [
    openssl
    libxcb
    alsa-lib
    wayland
    libxkbcommon
    fontconfig
    freetype
    mesa
    libGL
    libglvnd
    glib
    vulkan-loader
    vulkan-headers
    nss
    nspr
    atk
    at-spi2-atk
    at-spi2-core
    dbus
    cups
    libdrm
    libgbm
    libxshmfence
    udev
    expat
    cairo
    pango
    systemd
    xorg.libX11
    xorg.libXcomposite
    xorg.libXdamage
    xorg.libXext
    xorg.libXfixes
    xorg.libXrandr
    xorg.libXrender
    xorg.libXtst
    xorg.libxcb
    pciutils
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (
    with pkgs;
    [
      wayland
      libxkbcommon
      mesa
      libGL
      libglvnd
      glib
      vulkan-loader
      nss
      nspr
      atk
      dbus
      cups
      libdrm
      libgbm
      libxshmfence
      udev
      expat
      cairo
      pango
      systemd
      alsa-lib
      xorg.libX11
      xorg.libXcomposite
      xorg.libXdamage
      xorg.libXext
      xorg.libXfixes
      xorg.libXrandr
      xorg.libXrender
      xorg.libXtst
      xorg.libxcb
    ]
  );

  CARGO_BUILD_TARGET = rustTarget;
  CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER =
    if cross then "${pkgs.stdenv.cc}/bin/${pkgs.stdenv.cc.targetPrefix}cc" else "";
  PKG_CONFIG_ALLOW_CROSS = if cross then "1" else "0";

  shellHook = ''
    if [ -f .venv/bin/activate ]; then
      source .venv/bin/activate
    fi
    export REFLEX_USE_SYSTEM_BUN=True

    for profile in debug release; do
      if [ "${rustTarget}" = "x86_64-unknown-linux-gnu" ]; then
          target_dir="rustclock/target/$profile"
      else
          target_dir="rustclock/target/${rustTarget}/$profile"
      fi

      if [ -d "$target_dir" ]; then
        cef_dir=$(find rustclock/target -type d -name "cef_linux_*" | head -n 1)
        if [ -n "$cef_dir" ]; then
          ln -sf "$PWD/$cef_dir"/* "$target_dir/" 2>/dev/null || true
        fi
      fi
    done

    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$PWD/rustclock/target/debug:$PWD/rustclock/target/release:$PWD/rustclock/target/${rustTarget}/debug:$PWD/rustclock/target/${rustTarget}/release"
  '';
}
