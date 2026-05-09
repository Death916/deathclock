let
  nixconfig = builtins.getFlake "github:death916/nixconfig";
  unstable = nixconfig.inputs.nixpkgs-unstable.legacyPackages.x86_64-linux;
  pkgs = nixconfig.inputs.nixpkgs.legacyPackages.x86_64-linux;
in
pkgs.mkShell {
  packages = with pkgs; [
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
    pkgs.pkg-config
    pkgs.openssl
    pkgs.alsa-lib
    pkgs.libxcb
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
    pkgs.clippy
    # CEF Dependencies
    pkgs.nss
    pkgs.nspr
    pkgs.atk
    pkgs.at-spi2-atk
    pkgs.at-spi2-core
    pkgs.dbus
    pkgs.cups
    pkgs.libdrm
    pkgs.libgbm
    pkgs.expat
    pkgs.cairo
    pkgs.pango
    pkgs.systemd
    pkgs.alsa-lib
    pkgs.xorg.libX11
    pkgs.xorg.libXcomposite
    pkgs.xorg.libXdamage
    pkgs.xorg.libXext
    pkgs.xorg.libXfixes
    pkgs.xorg.libXrandr
    pkgs.xorg.libXtst
    pkgs.xorg.libxcb
    pkgs.pciutils
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.mesa
    pkgs.libGL
    pkgs.libglvnd
    pkgs.glib
    pkgs.vulkan-loader
    # CEF Runtime Libraries
    pkgs.nss
    pkgs.nspr
    pkgs.atk
    pkgs.at-spi2-atk
    pkgs.at-spi2-core
    pkgs.dbus
    pkgs.cups
    pkgs.libdrm
    pkgs.libgbm
    pkgs.expat
    pkgs.cairo
    pkgs.pango
    pkgs.systemd
    pkgs.alsa-lib
    pkgs.xorg.libX11
    pkgs.xorg.libXcomposite
    pkgs.xorg.libXdamage
    pkgs.xorg.libXext
    pkgs.xorg.libXfixes
    pkgs.xorg.libXrandr
    pkgs.xorg.libXtst
    pkgs.xorg.libxcb
  ];

  shellHook = ''
    source .venv/bin/activate
    # export PATH="${pkgs.bun}/bin:$PATH"
    # export BUN_INSTALL="${pkgs.bun}/bin/bun"
    export REFLEX_USE_SYSTEM_BUN=True
    echo venv activated and bun versions set
  '';
}
