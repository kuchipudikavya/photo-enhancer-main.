import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from enhancer.enhancer import Enhancer
import sys


def main(method: str, image_path: str, output_path: str, 
         background_enhancement: bool = True, upscale: int = 2) -> None:
    """
    Enhance an image using the specified method and save the result.
    
    Args:
        method: Enhancement method (gfpgan, RestoreFormer, codeformer)
        image_path: Path to input image
        output_path: Path to save enhanced image
        background_enhancement: Whether to enhance background (default: True)
        upscale: Upscale factor (default: 2)
        
    Raises:
        ValueError: If invalid arguments are provided
        FileNotFoundError: If input image doesn't exist
        IOError: If image can't be processed or saved
    """
    try:
        # Validate input file
        if not Path(image_path).is_file():
            raise FileNotFoundError(f"Input file not found: {image_path}")

        # Validate method
        valid_methods = ["gfpgan", "RestoreFormer", "codeformer"]
        if method.lower() not in valid_methods:
            raise ValueError(f"Invalid method. Must be one of: {', '.join(valid_methods)}")

        # Validate upscale
        if upscale not in [2, 4]:
            raise ValueError("Upscale must be either 2 or 4")

        # Create enhancer
        enhancer = Enhancer(
            method=method,
            background_enhancement=background_enhancement,
            upscale=upscale
        )

        # Process image
        with Image.open(image_path) as img:
            image = np.array(img.convert('RGB'))  # Ensure RGB format
            restored_image = enhancer.enhance(image)

        # Save output
        final_image = Image.fromarray(restered_image)
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)  # Create dirs if needed
        
        final_image.save(output_path)
        print(f"Successfully enhanced image saved to: {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Image Enhancement Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=["gfpgan", "RestoreFormer", "codeformer"],
        help="Enhancement method to use"
    )
    
    parser.add_argument(
        "--image_path",
        type=str,
        required=True,
        help="Path to input image file"
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to save enhanced image"
    )
    
    parser.add_argument(
        "--no-background_enhancement",
        dest="background_enhancement",
        action="store_false",
        help="Disable background enhancement"
    )
    
    parser.add_argument(
        "--upscale",
        type=int,
        choices=[2, 4],
        default=2,
        help="Upscaling factor"
    )
    
    args = parser.parse_args()
    
    main(
        method=args.method,
        image_path=args.image_path,
        output_path=args.output_path,
        background_enhancement=args.background_enhancement,
        upscale=args.upscale
    )