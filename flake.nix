{
  description = "A TUI app for playerctl playback control";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.05"; # Use nixos-unstable for latest packages
  };

  outputs = { self, nixpkgs }:
    let
      # Define the systems we want to build for
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];

      # Helper function to generate outputs for each system
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
    {
      # Dev shell for development (nix develop)
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonEnv = pkgs.python3.withPackages (p: [
            p.pip
            p.textual
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = [
              pythonEnv
              # playerctl is needed at runtime, so we add it to the shell
              pkgs.playerctl
            ];
            # Set up the PYTHONPATH so Python can find textual, etc.
            # And add the current directory to PATH so you can run python playerctl_tui.py
            shellHook = ''
              export PATH="$PWD/src:$PATH"
              # Optional: You might want to automatically run your app on entering the shell
              # echo "Type 'python playerctl_tui.py' to run the app."
              python playerctl_tui.py
            '';
          };
        }
      );

      # Application package (nix run .#playerctl-tui-app)
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonEnv = pkgs.python3.withPackages (p: [
            p.textual
          ]);
        in
        {
          playerctl-tui-app = pkgs.writeShellApplication {
            name = "playerctl-tui-app";
            runtimeInputs = [
              pythonEnv
              pkgs.playerctl # playerctl needs to be in the runtime path
            ];
            # The script to run your Python application
            text = ''
              exec "${pythonEnv}/bin/python" "${./src/playerctl_tui.py}" "$@"
            '';
          };
        }
      );

      # Default application to run (nix run .)
      apps = forAllSystems (system: {
        default = self.packages.${system}.playerctl-tui-app;
      });
    };
}
