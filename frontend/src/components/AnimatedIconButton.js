import React from 'react';
import { IconButton } from '@mui/material';
import { styled } from '@mui/material/styles';

export const AnimatedIconButton = styled(IconButton)(({ theme }) => ({
  width: 'auto',
  minWidth: 32,
  height: 38,
  borderRadius: 18,
  border: '1.2px solid #e0e0e2',
  background: '#fff',
  boxShadow: '0 1px 4px rgba(60,60,60,0.06)',
  fontSize: 18,
  transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
  overflow: 'hidden',
  paddingLeft: theme.spacing(1),
  paddingRight: `calc(${theme.spacing(1)} + 3px)`,
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(0.7),
  color: '#666',
  position: 'relative',
  '& .btn-label': {
    opacity: 0,
    maxWidth: 0,
    marginLeft: 0,
    transition: 'max-width 1.5s cubic-bezier(.4,2,.6,1), opacity 0.22s, margin-left 0.22s, color 0.22s',
    whiteSpace: 'nowrap',
    display: 'inline-block',
    color: '#666',
    fontWeight: 500,
    fontSize: 13,
    letterSpacing: 0.2,
    overflow: 'hidden',
  },
  '&:hover': {
    background: '#f3f3f4',
    boxShadow: '0 2px 8px rgba(60,60,60,0.10)',
    color: '#222',
    borderColor: '#bdbdbf',
  },
  '&:hover .btn-label': {
    opacity: 1,
    maxWidth: 200,
    marginLeft: theme.spacing(0.7),
    color: '#222',
  },
  '&:active': {
    background: '#ededee',
    boxShadow: 'none',
  },
  '&.Mui-disabled': {
    color: '#bbb',
    background: '#f5f5f7',
    boxShadow: 'none',
    opacity: 0.5,
    borderColor: '#e0e0e2',
  }
})); 