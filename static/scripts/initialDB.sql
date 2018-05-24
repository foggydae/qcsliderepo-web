create table file (
    Url varchar(100),
    FileName varchar(100),
    UploadDate varchar(100),
    UploaderContactInfo varchar(100),
    TissueType varchar(100),
    SlideCreationDate varchar(100),
    BaseMagnification varchar(100),
    ArtifactsTypes varchar(100),
    StainType varchar(100),
    Comments varchar(10000),
    ImageSizeInPixels varchar(100),
    ImageSizeInGB varchar(100),
    FileType varchar(100),
    Scanner varchar(100),
    PreparationType varchar(100),
    SpecimenType varchar(100)
) default charset = utf8;