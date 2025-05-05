import React, { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, MarkerF } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '600px',
  maxWidth: '800px', // Add max-width to prevent map from getting too wide
  margin: '0 auto' // Center the map
};

const center = {
  lat: 51.509865,
  lng: -0.118092
};

interface GroupUser {
  id: string;
  type: string;
  attributes: {
    address: string;
    first_name: string;
    second_name: string;
  };
}

const MapDisplay: React.FC = () => {
  const [userLocations, setUserLocations] = useState<{ lat: number; lng: number }[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const groupId = '036747a1a1634a5b9d978645f4e25261';

  useEffect(() => {
    const fetchGroupUsers = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`${import.meta.env.VITE_APP_BACKEND_ADDRESS}/api/v1/groups/${groupId}/users`);
        const data = await response.json();
        
        // Get coordinates for each user's address
        const locations = await Promise.all(
          data.included.map(async (user: GroupUser) => {
            const geocodeResponse = await fetch(
              `${import.meta.env.VITE_APP_BACKEND_ADDRESS}/api/v1/geocode?address=${encodeURIComponent(user.attributes.address)}`
            );
            return geocodeResponse.json();
          })
        );
        setUserLocations(locations);
      } catch (err) {
        console.error('Error fetching group users:', err);
        setError('Failed to load user locations');
      } finally {
        setIsLoading(false);
      }
    };

    fetchGroupUsers();
  }, [groupId]);

  if (isLoading) return <div className="flex justify-center p-4">Loading map...</div>;
  if (error) return <div className="text-red-500 p-4">Error: {error}</div>;

  return (
    <div className="container mx-auto px-4 max-w-7xl"> {/* Add container with padding */}
      <div className="my-4 rounded-lg overflow-hidden shadow-lg">
        <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={userLocations[0] || center}
            zoom={12}
          >
            {userLocations.map((location, index) => (
              <MarkerF
                key={index}
                position={location}
                title={`User ${index + 1}`}
              />
            ))}
          </GoogleMap>
        </LoadScript>
      </div>
    </div>
  );
};

export default MapDisplay;

