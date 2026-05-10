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
    pkgs.clippy
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
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.mesa
    pkgs.libGL
    pkgs.libglvnd
    pkgs.glib
    pkgs.vulkan-loader
    pkgs.nss
    pkgs.nspr
    pkgs.atk
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
    pkgs.alsa-lib
    pkgs.xorg.libX11
    pkgs.xorg.libXcomposite
    pkgs.xorg.libXdamage
    pkgs.xorg.libXext
    pkgs.xorg.libXfixes
    pkgs.xorg.libXrandr
    pkgs.xorg.libXrender
    pkgs.xorg.libXtst
    pkgs.xorg.libxcb
  ];

  shellHook = ''
    source .venv/bin/activate
    export REFLEX_USE_SYSTEM_BUN=True

    echo "Linking CEF resources to target folders..."
    for profile in debug release; do
      target_dir="rustclock/target/$profile"
      if [ -d "$target_dir" ]; then
        cef_dir=$(find rustclock/target/$profile/build -type d -name "cef_linux_x86_64" | head -n 1)
        if [ -n "$cef_dir" ]; then
          ln -sf "$PWD/$cef_dir"/* "$target_dir/" 2>/dev/null || true
        fi
      fi
    done
  '';
}
