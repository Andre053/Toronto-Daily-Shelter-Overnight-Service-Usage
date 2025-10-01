import { FeatureCollection } from "geojson";

export type AreaData = {
  [key: string]: string | string[] | any
}

export type GeoData = {
  name: string,
  featureCollection: FeatureCollection
}

export type ServerData = {
  message: string;
  data: any;
}

export type FsaData = {
    fsa: fsaCounts[];
    stats: FsaStats;
}

export type fsaCounts = {
  key: string;
  val: number;
}
export type FsaStats = {
  max: number;
}

export type OccupancyData = {
  occupancyDate: string;
  organizationName: string;
  shelterId: number;
  shelterGroup: string;
  locationName: string;
  locationAddress: string;
  locationPostalCode: string;
  locationCity: string;
  programId: number;
  programName: string;
  programModel: string;
  programSector: string;
  overnightServiceType: string;
}
