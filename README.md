# LineupTunes 🎵

An AWS Lambda function that automatically generates Spotify playlists from music festival lineups. Simply provide a list of artists and get an "Unofficial" playlist with their top tracks!

## Overview

LineupTunes takes the hassle out of discovering music from festival lineups by automatically creating Spotify playlists with top tracks from each artist. Perfect for music festival preparation, discovering new artists, or creating themed playlists.

## Features

- 🎪 Convert festival lineups into Spotify playlists
- 🎵 Automatically selects top tracks from each artist
- 🔧 Configurable number of songs per artist
- ☁️ Serverless architecture using AWS Lambda
- 🚀 Automated deployment with GitHub Actions

## Requirements

### AWS Services
- AWS Lambda
- AWS S3 (for deployment packages)
- AWS CloudFormation/SAM
- IAM roles and policies

### Development Tools
- Python 3.13
- AWS SAM CLI
- Git/GitHub account

### External Services
- Spotify Developer Account
- Spotify Web API credentials

## Setup Instructions

### 1. Spotify Developer Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your `Client ID` and `Client Secret`
4. Add `http://localhost:9000/callback` as a redirect URI

### 2. Get Spotify Authorization Code

Before invoking the Lambda function, you need to obtain an authorization code:

1. Open this URL in your browser (replace `YOUR_CLIENT_ID` with your actual Client ID):
```
https://accounts.spotify.com/authorize?response_type=code&client_id=YOUR_CLIENT_ID&scope=user-read-private user-read-email playlist-modify-public playlist-modify-private&redirect_uri=http://localhost:9000/callback
```

2. Authorize the application
3. Copy the `code` parameter from the callback URL - this is your auth code

### 3. AWS Setup

1. Install AWS SAM CLI:
```bash
pip install aws-sam-cli
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Set environment variables for the Lambda function:
   - `CLIENT_ID`: Your Spotify Client ID
   - `CLIENT_SECRET`: Your Spotify Client Secret

### 4. Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd lineuptunes
```

2. Install dependencies:
```bash
pip install requests
```

3. Build the SAM application:
```bash
sam build
```

4. Test locally (optional):
```bash
sam local invoke LineUpTunesLambda -e event.json
```

### 5. Deployment

#### Manual Deployment
```bash
sam deploy --guided
```

#### Automated Deployment (GitHub Actions)
The project includes GitHub Actions workflow for automatic deployment:

1. Set up GitHub repository secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`

2. Push changes to trigger deployment:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

## Usage

### Lambda Function Payload

Invoke the Lambda function with the following JSON payload:

```json
{
  "playlist_name": "Coachella 2024",
  "auth_code": "YOUR_SPOTIFY_AUTH_CODE",
  "number_of_songs_to_add": 3,
  "artist_list": [
    "Dua Lipa",
    "Tyler, The Creator", 
    "Arctic Monkeys",
    "Billie Eilish",
    "The Weeknd"
  ]
}
```

### Parameters

- **playlist_name** (string): Base name for your playlist (will append " - Unofficial")
- **auth_code** (string): Spotify authorization code obtained from setup step
- **number_of_songs_to_add** (integer): Number of top tracks to add per artist (1-10 recommended)
- **artist_list** (array): List of artist names to search for

### Example Response

The function will:
1. Create a public Spotify playlist named "{playlist_name} - Unofficial"
2. Search for each artist on Spotify
3. Add the specified number of top tracks from each artist
4. Log any artists that couldn't be found

The playlist will appear under the account you used to authorize the Spotify actions. They will appear under the public playlist section.

## Project Structure

```
lineuptunes/
├── app.py              # Main Lambda function
├── template.yml        # SAM CloudFormation template
├── requirements.txt    # Python dependencies
├── .github/
│   └── workflows/      # GitHub Actions deployment
└── README.md          # This file
```

## Error Handling

The function handles several error cases:
- Artists not found on Spotify are logged in `bad_search` array
- API rate limiting and HTTP errors are managed
- Invalid authorization codes will result in authentication failures

## Limitations

- Requires manual authorization code generation (expires after use)
- Limited to Spotify's search algorithm accuracy for artist matching
- Public playlists only (configurable in code)
- No duplicate track detection across artists

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with SAM
5. Submit a pull request

## License

[MIT License](https://github.com/mantzw/lineuptunes/blob/main/LICENSE)

## Troubleshooting

### Common Issues

**"Invalid authorization code"**
- Ensure you're using a fresh auth code
- Verify the redirect URI matches exactly

**"Artist not found"**
- Check artist name spelling
- Some artists may not be available on Spotify
- Try variations of the artist name

**"Deployment fails"**
- Verify AWS credentials and permissions
- Check CloudFormation stack events
- Ensure all environment variables are set

### Support

For issues and questions:
- Check the GitHub Issues page
- Review AWS CloudWatch logs for the Lambda function
- Verify Spotify API rate limits haven't been exceeded
